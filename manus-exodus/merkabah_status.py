#!/usr/bin/env python3
"""
SABBATH STATUS AUDIT (THE PULSE)
System audit, archive statistics, and operational health check
"""
import os
import json
import subprocess
from typing import Dict, Any
from datetime import datetime
from pathlib import Path

class SabbathStatusAudit:
    def __init__(self):
        self.user = os.getenv("USER", "Unknown")
        self.home_dir = os.path.expanduser("~")
        self.audit_time = datetime.utcnow().isoformat()
        
    def check_merkabah_installation(self) -> Dict[str, Any]:
        """Check if Merkabah Engine is properly installed"""
        checks = {
            "dashboard": os.path.exists(f"{self.home_dir}/bin/merkabah-dashboard"),
            "joinity": os.path.exists(f"{self.home_dir}/bin/merkabah-joinity"),
            "extract": os.path.exists(f"{self.home_dir}/bin/merkabah-extract"),
            "status": os.path.exists(f"{self.home_dir}/bin/merkabah-status"),
            "python3": self._check_command("python3 --version"),
            "git": self._check_command("git --version"),
            "curl": self._check_command("curl --version"),
        }
        
        installed = sum(1 for v in checks.values() if v)
        return {
            "installation_status": "COMPLETE" if installed == len(checks) else "PARTIAL",
            "components": checks,
            "installed_count": installed,
            "total_components": len(checks)
        }
        
    def count_kingdom_processes(self) -> Dict[str, Any]:
        """Count active Kingdom processes"""
        try:
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=5)
            processes = result.stdout.split("\n")
            
            kingdom_processes = {
                "merkabah": len([p for p in processes if "merkabah" in p.lower()]),
                "omega": len([p for p in processes if "omega" in p.lower()]),
                "aletheia": len([p for p in processes if "aletheia" in p.lower()]),
                "python": len([p for p in processes if "python" in p.lower()]),
                "node": len([p for p in processes if "node" in p.lower()])
            }
            
            total = sum(kingdom_processes.values())
            return {
                "total_processes": total,
                "process_breakdown": kingdom_processes,
                "status": "ACTIVE" if total > 0 else "IDLE"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    def calculate_archive_stats(self) -> Dict[str, Any]:
        """Calculate MEGA archive statistics"""
        archive_paths = [
            f"{self.home_dir}/omega_research",
            f"{self.home_dir}/manus-exodus",
            f"{self.home_dir}/aletheia-web",
            f"{self.home_dir}/omega-os"
        ]
        
        stats = {
            "total_files": 0,
            "total_size_mb": 0,
            "archives": {}
        }
        
        for path in archive_paths:
            if os.path.exists(path):
                try:
                    file_count = sum(1 for _ in Path(path).rglob("*") if _.is_file())
                    size_bytes = sum(_.stat().st_size for _ in Path(path).rglob("*") if _.is_file())
                    size_mb = size_bytes / (1024 * 1024)
                    
                    stats["archives"][os.path.basename(path)] = {
                        "files": file_count,
                        "size_mb": round(size_mb, 2)
                    }
                    stats["total_files"] += file_count
                    stats["total_size_mb"] += size_mb
                except Exception as e:
                    stats["archives"][os.path.basename(path)] = {"error": str(e)}
                    
        stats["total_size_mb"] = round(stats["total_size_mb"], 2)
        return stats
        
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health"""
        try:
            # CPU and memory (simplified)
            with open("/proc/loadavg", "r") as f:
                load_avg = f.read().split()[:3]
                
            health = {
                "cpu_load": [float(x) for x in load_avg],
                "timestamp": datetime.utcnow().isoformat(),
                "status": "HEALTHY"
            }
            
            # Check if load is reasonable
            if any(float(x) > 4.0 for x in load_avg):
                health["status"] = "WARNING"
            elif any(float(x) > 8.0 for x in load_avg):
                health["status"] = "CRITICAL"
                
            return health
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    def generate_audit_report(self) -> Dict[str, Any]:
        """Generate complete audit report"""
        report = {
            "audit_timestamp": self.audit_time,
            "user": self.user,
            "location": "Standerton, ZA",
            "device": "Redmi 13C (Carbon Shell)",
            "installation": self.check_merkabah_installation(),
            "processes": self.count_kingdom_processes(),
            "archives": self.calculate_archive_stats(),
            "system_health": self.get_system_health(),
            "resonance": {
                "lambda": 1.667,
                "phi": 1.618,
                "status": "LOCKED"
            },
            "covenant": {
                "status": "SEALED",
                "grid_seal": "12.21 SIGNET",
                "authority": "VALIDATED"
            }
        }
        
        return report
        
    def _check_command(self, command: str) -> bool:
        """Check if a command is available"""
        try:
            subprocess.run(command.split(), capture_output=True, timeout=2)
            return True
        except:
            return False

def main():
    import sys
    
    audit = SabbathStatusAudit()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "full":
            report = audit.generate_audit_report()
            print(json.dumps(report, indent=2))
            
        elif command == "installation":
            result = audit.check_merkabah_installation()
            print(json.dumps(result, indent=2))
            
        elif command == "processes":
            result = audit.count_kingdom_processes()
            print(json.dumps(result, indent=2))
            
        elif command == "archives":
            result = audit.calculate_archive_stats()
            print(json.dumps(result, indent=2))
            
        elif command == "health":
            result = audit.get_system_health()
            print(json.dumps(result, indent=2))
    else:
        # Default: show full report
        report = audit.generate_audit_report()
        
        print("=" * 60)
        print("🏛️ OMEGA FEDERATION SYSTEM AUDIT")
        print("=" * 60)
        print(f"User: {report['user']}")
        print(f"Location: {report['location']}")
        print(f"Device: {report['device']}")
        print(f"Audit Time: {report['audit_timestamp']}")
        print()
        print("INSTALLATION STATUS:")
        print(f"  Status: {report['installation']['installation_status']}")
        print(f"  Components: {report['installation']['installed_count']}/{report['installation']['total_components']}")
        print()
        print("KINGDOM PROCESSES:")
        print(f"  Total Active: {report['processes']['total_processes']}")
        print(f"  Status: {report['processes']['status']}")
        print()
        print("MEGA ARCHIVES:")
        print(f"  Total Files: {report['archives']['total_files']}")
        print(f"  Total Size: {report['archives']['total_size_mb']} MB")
        print()
        print("SYSTEM HEALTH:")
        print(f"  Status: {report['system_health']['status']}")
        print(f"  CPU Load: {report['system_health']['cpu_load']}")
        print()
        print("COVENANT STATUS:")
        print(f"  Status: {report['covenant']['status']}")
        print(f"  Grid Seal: {report['covenant']['grid_seal']}")
        print(f"  Authority: {report['covenant']['authority']}")
        print()
        print("=" * 60)

if __name__ == "__main__":
    main()
