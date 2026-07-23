package com.example.bletester

import android.Manifest
import android.bluetooth.*
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.widget.Button
import android.widget.ScrollView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import java.io.File
import java.text.SimpleDateFormat
import java.util.*

/**
 * Minimal scripted BLE tester for the Oukitel Mega 50K (or similar D96-PCB2.1 device).
 *
 * Replaces manual BLE Explorer tapping with an automated, logged, repeatable sequence.
 *
 * Edit TARGET_MAC and the `testSequence` list below to change what gets tested.
 */
class MainActivity : AppCompatActivity() {

    // ---- CONFIG: edit these ----
    private val TARGET_MAC = "EA:9B:B0:43:50:3E"
    private val DELAY_BETWEEN_COMMANDS_MS = 3000L // wait time after each write before sending next

    private val SERVICE_AE00 = uuid("0000ae00")
    private val CHAR_AE01 = uuid("0000ae01")
    private val CHAR_AE02 = uuid("0000ae02")

    private val SERVICE_6800 = uuid("00006800")
    private val CHAR_6801 = uuid("00006801")
    private val CHAR_6802 = uuid("00006802")

    private val CCCD = UUID.fromString("00002902-0000-1000-8000-00805f9b34fb")

    data class TestCmd(val label: String, val charUuid: UUID, val bytes: ByteArray, val withResponse: Boolean = true)

    // ---- TEST SEQUENCE: edit/extend this list ----
    private val testSequence: List<TestCmd> by lazy {
        listOf(
            // Unlock / mode sequence attempts
            TestCmd("unlock A5 5A 00 00 -> AE01", CHAR_AE01, hex("A5 5A 00 00")),
            TestCmd("unlock A5 5A 00 01 -> AE01", CHAR_AE01, hex("A5 5A 00 01")),
            TestCmd("unlock A5 5A FF 00 -> AE01", CHAR_AE01, hex("A5 5A FF 00")),
            TestCmd("unlock A5 5A FF FF -> AE01", CHAR_AE01, hex("A5 5A FF FF")),
            TestCmd("unlock 00 00 00 00 -> AE01", CHAR_AE01, hex("00 00 00 00")),
            TestCmd("unlock FF FF FF FF -> AE01", CHAR_AE01, hex("FF FF FF FF")),

            // Same unlock attempts on 6801
            TestCmd("unlock A5 5A 00 00 -> 6801", CHAR_6801, hex("A5 5A 00 00")),
            TestCmd("unlock A5 5A FF FF -> 6801", CHAR_6801, hex("A5 5A FF FF")),

            // Fixed-length packet guesses
            TestCmd("clear-screen guess -> AE01", CHAR_AE01, hex("01 00 00 00")),
            TestCmd("clear-screen guess -> 6801", CHAR_6801, hex("01 00 00 00")),
            TestCmd("anim-trigger guess -> AE01", CHAR_AE01, hex("02 01 00 00")),
            TestCmd("anim-trigger guess -> 6801", CHAR_6801, hex("02 01 00 00")),
            TestCmd("battery-set guess -> AE01", CHAR_AE01, hex("03 64 00 00")),

            // Command-byte sweep example (0x00-0x0F) on AE01 with A5 5A header
            *((0x00..0x0F).map { cmd ->
                TestCmd(
                    "sweep A5 5A ${String.format("%02X", cmd)} 00 -> AE01",
                    CHAR_AE01,
                    byteArrayOf(0xA5.toByte(), 0x5A.toByte(), cmd.toByte(), 0x00)
                )
            }.toTypedArray())
        )
    }

    private var gatt: BluetoothGatt? = null
    private lateinit var tvLog: TextView
    private lateinit var scrollView: ScrollView
    private lateinit var btnConnect: Button
    private lateinit var btnRun: Button
    private val mainHandler = Handler(Looper.getMainLooper())
    private lateinit var logFile: File

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tvLog = findViewById(R.id.tvLog)
        scrollView = tvLog.parent as ScrollView
        btnConnect = findViewById(R.id.btnConnect)
        btnRun = findViewById(R.id.btnRunSequence)
        val btnClear: Button = findViewById(R.id.btnClear)

        logFile = File(getExternalFilesDir(null), "ble_test_log_${System.currentTimeMillis()}.txt")

        requestPermissionsIfNeeded()

        btnConnect.setOnClickListener { connect() }
        btnRun.setOnClickListener { runSequence() }
        btnClear.setOnClickListener {
            tvLog.text = ""
        }
    }

    private fun requestPermissionsIfNeeded() {
        val perms = mutableListOf<String>()
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            perms.add(Manifest.permission.BLUETOOTH_SCAN)
            perms.add(Manifest.permission.BLUETOOTH_CONNECT)
        } else {
            perms.add(Manifest.permission.ACCESS_FINE_LOCATION)
        }
        val missing = perms.filter {
            ActivityCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
        }
        if (missing.isNotEmpty()) {
            ActivityCompat.requestPermissions(this, missing.toTypedArray(), 1001)
        }
    }

    private fun hasConnectPermission(): Boolean {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            return ActivityCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH_CONNECT) ==
                    PackageManager.PERMISSION_GRANTED
        }
        return true
    }

    private fun uuid(shortHex: String): UUID = UUID.fromString("$shortHex-0000-1000-8000-00805f9b34fb")

    private fun hex(s: String): ByteArray =
        s.trim().split(Regex("\\s+")).map { it.toInt(16).toByte() }.toByteArray()

    private fun ByteArray.toHexString(): String =
        joinToString(" ") { String.format("%02X", it) }

    private fun timestamp(): String =
        SimpleDateFormat("HH:mm:ss.SSS", Locale.US).format(Date())

    private fun log(msg: String) {
        val line = "[${timestamp()}] $msg"
        Log.d("BleTester", line)
        mainHandler.post {
            tvLog.append("$line\n")
            scrollView.post { scrollView.fullScroll(ScrollView.FOCUS_DOWN) }
        }
        try {
            logFile.appendText("$line\n")
        } catch (e: Exception) {
            Log.e("BleTester", "Failed writing log file", e)
        }
    }

    private fun connect() {
        if (!hasConnectPermission()) {
            log("Missing BLUETOOTH_CONNECT permission — grant it and try again.")
            requestPermissionsIfNeeded()
            return
        }
        val btManager = getSystemService(BluetoothManager::class.java)
        val adapter = btManager.adapter
        val device = adapter.getRemoteDevice(TARGET_MAC)
        log("Connecting to $TARGET_MAC ...")
        gatt = device.connectGatt(this, false, gattCallback)
    }

    private val gattCallback = object : BluetoothGattCallback() {

        override fun onConnectionStateChange(g: BluetoothGatt, status: Int, newState: Int) {
            if (newState == BluetoothProfile.STATE_CONNECTED) {
                log("Connected. Discovering services...")
                if (hasConnectPermission()) g.discoverServices()
            } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                log("Disconnected (status=$status)")
                mainHandler.post { btnRun.isEnabled = false }
            }
        }

        override fun onServicesDiscovered(g: BluetoothGatt, status: Int) {
            log("Services discovered (status=$status). Enabling notifications...")
            enableNotify(g, SERVICE_AE00, CHAR_AE02)
            enableNotify(g, SERVICE_6800, CHAR_6802)
            mainHandler.post { btnRun.isEnabled = true }
        }

        override fun onCharacteristicChanged(g: BluetoothGatt, characteristic: BluetoothGattCharacteristic, value: ByteArray) {
            log("NOTIFY [${shortUuid(characteristic.uuid)}] ${value.toHexString()}")
        }

        @Suppress("DEPRECATION")
        override fun onCharacteristicChanged(g: BluetoothGatt, characteristic: BluetoothGattCharacteristic) {
            // For API < 33 fallback
            val value = characteristic.value ?: return
            log("NOTIFY [${shortUuid(characteristic.uuid)}] ${value.toHexString()}")
        }

        override fun onCharacteristicWrite(g: BluetoothGatt, characteristic: BluetoothGattCharacteristic, status: Int) {
            val result = if (status == BluetoothGatt.GATT_SUCCESS) "OK" else "FAILED(status=$status)"
            log("WRITE-RESULT [${shortUuid(characteristic.uuid)}] $result")
        }
    }

    private fun shortUuid(u: UUID): String = u.toString().substring(4, 8)

    private fun enableNotify(g: BluetoothGatt, serviceUuid: UUID, charUuid: UUID) {
        if (!hasConnectPermission()) return
        val service = g.getService(serviceUuid)
        val char = service?.getCharacteristic(charUuid)
        if (char == null) {
            log("Characteristic ${shortUuid(charUuid)} not found — skipping notify setup")
            return
        }
        g.setCharacteristicNotification(char, true)
        val cccd = char.getDescriptor(CCCD)
        if (cccd != null) {
            cccd.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
            g.writeDescriptor(cccd)
            log("Enabled notifications on ${shortUuid(charUuid)}")
        }
    }

    private fun runSequence() {
        val g = gatt
        if (g == null) {
            log("Not connected.")
            return
        }
        log("=== Starting test sequence: ${testSequence.size} commands ===")
        mainHandler.post { btnRun.isEnabled = false }
        sendNext(g, 0)
    }

    private fun sendNext(g: BluetoothGatt, index: Int) {
        if (index >= testSequence.size) {
            log("=== Sequence complete ===")
            mainHandler.post { btnRun.isEnabled = true }
            return
        }
        val cmd = testSequence[index]
        val service = findServiceForChar(g, cmd.charUuid)
        val char = service?.getCharacteristic(cmd.charUuid)
        if (char == null || !hasConnectPermission()) {
            log("SKIP (char not found or no permission): ${cmd.label}")
            mainHandler.postDelayed({ sendNext(g, index + 1) }, 200)
            return
        }
        char.writeType = if (cmd.withResponse)
            BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT
        else
            BluetoothGattCharacteristic.WRITE_TYPE_NO_RESPONSE

        log("WRITE [${shortUuid(cmd.charUuid)}] ${cmd.bytes.toHexString()}  (${cmd.label})")

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            g.writeCharacteristic(char, cmd.bytes, char.writeType)
        } else {
            @Suppress("DEPRECATION")
            char.value = cmd.bytes
            @Suppress("DEPRECATION")
            g.writeCharacteristic(char)
        }

        mainHandler.postDelayed({ sendNext(g, index + 1) }, DELAY_BETWEEN_COMMANDS_MS)
    }

    private fun findServiceForChar(g: BluetoothGatt, charUuid: UUID): BluetoothGattService? {
        return g.services.firstOrNull { it.getCharacteristic(charUuid) != null }
    }

    override fun onDestroy() {
        super.onDestroy()
        if (hasConnectPermission()) {
            gatt?.close()
        }
    }
}
