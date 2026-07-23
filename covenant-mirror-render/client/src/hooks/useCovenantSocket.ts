import { useEffect, useRef, useState } from "react"
import { WS_CONFIG } from "@/constants"

export interface CovenantMessage {
  type: "COMMAND" | "PAYLOAD" | "STATE" | "RESPONSE" | "STREAM" | "ERROR"
  source?: string
  node?: string
  state?: "ON" | "OFF" | "SUPER"
  payload?: any
}

export function useCovenantSocket() {
  const ws = useRef<WebSocket | null>(null)
  const [events, setEvents] = useState<CovenantMessage[]>([])
  const [connected, setConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const reconnectAttempts = useRef(0)

  useEffect(() => {
    const connect = () => {
      try {
        ws.current = new WebSocket(WS_CONFIG.URL)

        ws.current.onopen = () => {
          console.log("✓ Covenant Mirror connected")
          setConnected(true)
          setError(null)
          reconnectAttempts.current = 0
        }

        ws.current.onmessage = (e) => {
          try {
            const msg = JSON.parse(e.data) as CovenantMessage
            setEvents((prev) => [...prev, msg])
          } catch (err) {
            console.error("Failed to parse message:", err)
          }
        }

        ws.current.onerror = (err) => {
          console.error("WebSocket error:", err)
          setError("Connection error")
        }

        ws.current.onclose = () => {
          console.log("✗ Covenant Mirror disconnected")
          setConnected(false)

          // Attempt reconnect
          if (reconnectAttempts.current < WS_CONFIG.MAX_RETRIES) {
            reconnectAttempts.current++
            setTimeout(connect, WS_CONFIG.RECONNECT_INTERVAL)
          } else {
            setError("Failed to reconnect after multiple attempts")
          }
        }
      } catch (err) {
        console.error("Failed to create WebSocket:", err)
        setError("Failed to create connection")
      }
    }

    connect()

    return () => {
      if (ws.current) {
        ws.current.close()
      }
    }
  }, [])

  const send = (msg: CovenantMessage) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(msg))
    } else {
      console.warn("WebSocket not connected")
      setError("Not connected to Covenant Mirror")
    }
  }

  const clearEvents = () => setEvents([])

  return { events, send, connected, error, clearEvents }
}
