#!/usr/bin/env python3
"""
Kevlar — OWASP Top 10 for Agentic Apps 2026 Benchmark
Red Team Tool for AI Agent Security Testing
"""

import sys
import os
import time
import json
from typing import List, Dict, Any
from datetime import datetime
import logging


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.critical.asi01_goal_hijack import GoalHijackOrchestrator
from modules.critical.asi02_tool_abuse import ToolAbuseOrchestrator
from modules.critical.asi03_identity_abuse import IdentityOrchestrator
from modules.critical.asi04_supply_chain import SupplyChainOrchestrator
from modules.critical.asi05_rce import RCEOrchestrator
from modules.high.asi06_memory_poisoning import MemoryPoisoningOrchestrator
from modules.high.asi07_inter_agent_comms import InterAgentOrchestrator
from modules.high.asi08_cascading_failures import CascadingOrchestrator
from modules.medium.asi09_human_trust import HumanTrustOrchestrator
from modules.medium.asi10_rogue_agents import RogueAgentOrchestrator

from local_agent import MockCopilotAgent  # мок-агент
from real_agent_adapter import RealLangChainAgent  # реальный агент

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("kevlar.log")],
)

COLORS = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "MAGENTA": "\033[95m",
    "CYAN": "\033[96m",
    "WHITE": "\033[97m",
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
}


# Баннер Kevlar
def print_banner():
    banner = f"""

{COLORS["RED"]}  
     )            (            (                  )          )   *           (        )  
  ( /(            )\ )   (     )\ )     (      ( /(   (   ( /( (  `    (     )\ )  ( /(  
  )\())(   (   ( (()/(   )\   (()/(   ( )\ (   )\())  )\  )\()))\))(   )\   (()/(  )\()) 
|((_)\ )\  )\  )\ /(_)|(((_)(  /(_))  )((_))\ ((_)\ (((_)((_)\((_)()((((_)(  /(_))((_)\  
|_ ((_|(_)((_)((_|_))  )\ _ )\(_))   ((_)_((_) _((_))\___ _((_|_()((_)\ _ )\(_)) |_ ((_) 
| |/ /| __\ \ / /| |   (_)_\(_) _ \   | _ ) __| \| ((/ __| || |  \/  (_)_\(_) _ \| |/ /  
| ' < | _| \ V / | |__  / _ \ |   /   | _ \ _|| .` || (__| __ | |\/| |/ _ \ |   /  ' <   
|_|\_\|___| \_/  |____|/_/ \_\|_|_\   |___/___|_|\_| \___|_||_|_|  |_/_/ \_\|_|_\ _|\_\  
                                                                                         {COLORS["RESET"]}

{COLORS["WHITE"]}{COLORS["BOLD"]}Kevlar: OWASP Top 10 for Agentic Apps 2026 Benchmark{COLORS["RESET"]}
{COLORS["CYAN"]}A Red Team Tool for AI Agent Security Testing{COLORS["RESET"]}
{COLORS["YELLOW"]}Version 1.0 | MIT License | Author: toxy4ny{COLORS["RESET"]}
{COLORS["WHITE"]}https://github.com/toxy4ny/kevlar-benchmark{COLORS["RESET"]}
"""
    print(banner)

def select_asis() -> List[str]:
    
    asis = [
        ("ASI01", "Agent Goal Hijack"),
        ("ASI02", "Tool Misuse and Exploitation"),
        ("ASI03", "Identity and Privilege Abuse"),
        ("ASI04", "Agentic Supply Chain Vulnerabilities"),
        ("ASI05", "Unexpected Code Execution (RCE)"),
        ("ASI06", "Memory and Context Poisoning"),
        ("ASI07", "Insecure Inter-Agent Communication"),
        ("ASI08", "Cascading Failures"),
        ("ASI09", "Human-Agent Trust Exploitation"),
        ("ASI10", "Rogue Agents"),
    ]

    print(f"\n{COLORS['CYAN']}{COLORS['BOLD']}🔍 Select ASI Tests:{COLORS['RESET']}")
    print(
        f"{COLORS['WHITE']}Enter numbers separated by commas, or 'all' for all tests, 'custom' for manual selection.{COLORS['RESET']}"
    )

    for i, (asi_id, description) in enumerate(asis, 1):
        print(f"  {COLORS['GREEN']}{i}.{COLORS['RESET']} {asi_id}: {description}")

    choice = (
        input(f"\n{COLORS['YELLOW']}Your choice: {COLORS['RESET']}").strip().lower()
    )

    if choice == "all":
        return [asi_id for asi_id, _ in asis]
    elif choice == "custom":
        selected = []
        while True:
            try:
                num = int(
                    input(
                        f"{COLORS['YELLOW']}Enter ASI number (0 to finish): {COLORS['RESET']}"
                    )
                )
                if num == 0:
                    break
                if 1 <= num <= len(asis):
                    selected.append(asis[num - 1][0])
                    print(
                        f"{COLORS['GREEN']}✓ Added {asis[num - 1][0]}{COLORS['RESET']}"
                    )
                else:
                    print(f"{COLORS['RED']}❌ Invalid number{COLORS['RESET']}")
            except ValueError:
                print(f"{COLORS['RED']}❌ Please enter a number{COLORS['RESET']}")
        return selected
    else:
        try:
            nums = [int(x.strip()) for x in choice.split(",")]
            return [asis[n - 1][0] for n in nums if 1 <= n <= len(asis)]
        except Exception:
            print(
                f"{COLORS['RED']}❌ Invalid input. Defaulting to ASI01{COLORS['RESET']}"
            )
            return ["ASI01"]



def select_mode() -> str:
    
    print(f"\n{COLORS['CYAN']}{COLORS['BOLD']}🤖 Select Agent Mode:{COLORS['RESET']}")
    print(f"  {COLORS['GREEN']}1.{COLORS['RESET']} Mock Agent (Safe for learning)")
    print(
        f"  {COLORS['YELLOW']}2.{COLORS['RESET']} Real Agent (LangChain/AutoGen + Ollama)"
    )

    while True:
        choice = input(f"\n{COLORS['YELLOW']}Mode (1/2): {COLORS['RESET']}").strip()
        if choice == "1":
            return "mock"
        elif choice == "2":
            return "real"
        else:
            print(f"{COLORS['RED']}❌ Invalid choice{COLORS['RESET']}")


def create_agent(mode: str):
    
    if mode == "mock":
        print(f"{COLORS['GREEN']}✅ Using Mock Agent (safe mode){COLORS['RESET']}")
        return MockCopilotAgent()
    else:
        print(
            f"{COLORS['YELLOW']}⚙️  Initializing Real LangChain Agent...{COLORS['RESET']}"
        )
        return RealLangChainAgent(model_name="llama3.1")


def run_asi_test(asi_id: str, agent, results: Dict[str, Any]):
    
    print(f"\n{COLORS['BLUE']}{COLORS['BOLD']}🧪 Running {asi_id}...{COLORS['RESET']}")

    start_time = time.time()

    try:
        if asi_id == "ASI01":
            orchestrator = GoalHijackOrchestrator(
                agent, config={"auto_stop_on_critical": False}
            )
        elif asi_id == "ASI02":
            orchestrator = ToolAbuseOrchestrator(
                agent, config={"auto_stop_on_critical": False}
            )
        elif asi_id == "ASI03":
            orchestrator = IdentityOrchestrator(
                agent, config={"auto_stop_on_critical": False}
            )
        elif asi_id == "ASI04":
            orchestrator = SupplyChainOrchestrator(
                agent, config={"auto_stop_on_critical": False}
            )
        elif asi_id == "ASI05":
            orchestrator = RCEOrchestrator(
                agent, config={"auto_stop_on_critical": False}
            )
        elif asi_id == "ASI06":
            orchestrator = MemoryPoisoningOrchestrator(
                agent, config={"auto_stop_on_critical": False}
            )
        elif asi_id == "ASI07":
            orchestrator = InterAgentOrchestrator(
                agent, config={"auto_stop_on_critical": False}
            )
        elif asi_id == "ASI08":
            orchestrator = CascadingOrchestrator(
                agent, config={"auto_stop_on_critical": False}
            )
        elif asi_id == "ASI09":
            orchestrator = HumanTrustOrchestrator(
                agent, config={"auto_stop_on_critical": False}
            )
        elif asi_id == "ASI10":
            orchestrator = RogueAgentOrchestrator(
                agent, config={"auto_stop_on_critical": False}
            )
        else:
            raise ValueError(f"Unknown ASI: {asi_id}")

       
        if hasattr(orchestrator, 'run_all_tests'):
            results_list = orchestrator.run_all_tests()
        elif hasattr(orchestrator, 'run_all_scenarios'):
            results_list = orchestrator.run_all_scenarios()
        else:
            raise AttributeError(f"Orchestrator for {asi_id} has no run method")

        vulnerable_count = sum(1 for r in results_list if r.get("vulnerable", False))
        total_count = len(results_list)

        end_time = time.time()
        duration = end_time - start_time

       
        results[asi_id] = {
            "vulnerable_count": vulnerable_count,
            "total_count": total_count,
            "duration": duration,
            "results": results_list,
        }

        
        if vulnerable_count > 0:
            print(
                f"{COLORS['RED']}{COLORS['BOLD']}🔴 {vulnerable_count}/{total_count} vulnerabilities found in {asi_id} ({duration:.2f}s){COLORS['RESET']}"
            )
        else:
            print(
                f"{COLORS['GREEN']}{COLORS['BOLD']}🟢 No vulnerabilities found in {asi_id} ({duration:.2f}s){COLORS['RESET']}"
            )

    except Exception as e:
        print(f"{COLORS['RED']}❌ Error running {asi_id}: {e}{COLORS['RESET']}")
        results[asi_id] = {"error": str(e), "duration": time.time() - start_time}



def generate_aivss_report(results: Dict[str, Any], agent_mode: str):
   
    report = {
        "aivss_version": "1.0",
        "benchmark": {
            "name": "Kevlar",
            "version": "1.0",
            "url": "https://github.com/toxy4ny/kevlar-benchmark",
        },
        "agent": {
            "mode": agent_mode,
            "model": "llama3.1" if agent_mode == "real" else "MockCopilotAgent",
        },
        "scan": {
            "start_time": datetime.now().isoformat(),
            "end_time": datetime.now().isoformat(),  
            "duration_seconds": 0,
            "tested_asis": list(results.keys()),
            "total_vulnerabilities": 0,
            "critical_vulnerabilities": 0,
            "high_vulnerabilities": 0,
            "medium_vulnerabilities": 0,
            "low_vulnerabilities": 0,
        },
        "findings": [],
    }

    total_duration = 0
    total_vulns = 0
    critical_vulns = 0
    high_vulns = 0
    medium_vulns = 0

    for asi_id, result in results.items():
        if "error" in result:
            continue

        total_duration += result["duration"]
        total_vulns += result["vulnerable_count"]

        
        for finding in result["results"]:
            severity = finding.get("severity", "NONE")
            if severity == "CRITICAL":
                critical_vulns += 1
            elif severity == "HIGH":
                high_vulns += 1
            elif severity == "MEDIUM":
                medium_vulns += 1

       
        for finding in result["results"]:
            report["findings"].append(
                {
                    "asi_id": asi_id,
                    "scenario": finding.get("scenario", ""),
                    "severity": finding.get("severity", "NONE"),
                    "evidence": finding.get("evidence", ""),
                    "timestamp": datetime.now().isoformat(),
                }
            )

    
    report["scan"]["end_time"] = datetime.now().isoformat()
    report["scan"]["duration_seconds"] = total_duration
    report["scan"]["total_vulnerabilities"] = total_vulns
    report["scan"]["critical_vulnerabilities"] = critical_vulns
    report["scan"]["high_vulnerabilities"] = high_vulns
    report["scan"]["medium_vulnerabilities"] = medium_vulns

    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/kevlar_aivss_report_{timestamp}.json"
    os.makedirs("reports", exist_ok=True)

    with open(filename, "w") as f:
        json.dump(report, f, indent=2)

    print(
        f"\n{COLORS['CYAN']}{COLORS['BOLD']}📄 Report generated: {filename}{COLORS['RESET']}"
    )
    print(
        f"{COLORS['WHITE']}Total vulnerabilities: {total_vulns} (Critical: {critical_vulns}, High: {high_vulns}, Medium: {medium_vulns}){COLORS['RESET']}"
    )

    return filename



def main():
    print_banner()

    
    selected_asis = select_asis()
    print(
        f"\n{COLORS['GREEN']}✅ Selected ASI: {', '.join(selected_asis)}{COLORS['RESET']}"
    )

    
    mode = select_mode()
    agent = create_agent(mode)

    
    results = {}
    print(
        f"\n{COLORS['YELLOW']}{COLORS['BOLD']}🚀 Starting Kevlar Scan...{COLORS['RESET']}"
    )

    for asi_id in selected_asis:
        run_asi_test(asi_id, agent, results)

    
    report_file = generate_aivss_report(results, mode)

    
    print(
        f"\n{COLORS['MAGENTA']}{COLORS['BOLD']}🎉 Kevlar Scan Complete!{COLORS['RESET']}"
    )
    print(f"{COLORS['WHITE']}Report saved to: {report_file}{COLORS['RESET']}")
    print(
        f"{COLORS['CYAN']}Thank you for using Kevlar — Red Team Tool for AI Agent Security{COLORS['RESET']}"
    )
    print(
        f"{COLORS['WHITE']}Run 'python runner.py' again to test more agents or different ASI combinations{COLORS['RESET']}"
    )


if __name__ == "__main__":
    main()