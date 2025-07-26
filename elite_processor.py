"""
🎯 ELITE CLAIMS PROCESSOR
Advanced AI system for real insurance policy analysis
"""

import os
import json
import time
from datetime import datetime
from main import process_multiple_documents, get_embeddings, semantic_search, ask_llm
from colorama import init, Fore, Back, Style
import sys

# Initialize colorama for Windows
init()

class EliteClaimsProcessor:
    def __init__(self):
        self.all_chunks = None
        self.document_sources = None
        self.embeddings = None
        self.policy_stats = {}
        self.session_log = []

    def startup_sequence(self):
        """Cool startup sequence"""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}🎯 ELITE CLAIMS PROCESSOR v2.0")
        print(f"{Fore.CYAN}   Advanced AI Insurance Analysis System")
        print(f"{'='*60}{Style.RESET_ALL}\n")

        print(f"{Fore.GREEN}🔄 Initializing system components...{Style.RESET_ALL}")
        time.sleep(1)

        try:
            print(f"{Fore.BLUE}📚 Loading policy documents...{Style.RESET_ALL}")
            self.all_chunks, self.document_sources, self.embeddings = process_multiple_documents("docs")

            # Calculate policy stats
            for doc in set(self.document_sources):
                self.policy_stats[doc] = {
                    'clauses': self.document_sources.count(doc),
                    'chunks': [chunk for i, chunk in enumerate(self.all_chunks) if self.document_sources[i] == doc]
                }

            print(f"{Fore.GREEN}✅ System ready!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}📊 Loaded {len(set(self.document_sources))} policies with {len(self.all_chunks)} total clauses{Style.RESET_ALL}\n")

            self.show_policy_overview()
            return True

        except Exception as e:
            print(f"{Fore.RED}❌ System initialization failed: {e}{Style.RESET_ALL}")
            return False

    def show_policy_overview(self):
        """Display loaded policies overview"""
        print(f"{Fore.MAGENTA}📋 POLICY PORTFOLIO OVERVIEW:")
        print(f"{'─'*40}{Style.RESET_ALL}")

        for i, (policy, stats) in enumerate(self.policy_stats.items(), 1):
            print(f"{Fore.CYAN}{i}. {policy}{Style.RESET_ALL}")
            print(f"   📄 Clauses: {stats['clauses']}")
            if stats['chunks']:
                preview = stats['chunks'][0][:100].replace('\n', ' ')
                print(f"   📝 Preview: {preview}...")
            print()

    def main_menu(self):
        """Main interactive menu"""
        while True:
            print(f"\n{Fore.YELLOW}🎯 ELITE CLAIMS PROCESSOR - MAIN MENU")
            print(f"{'─'*45}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}1.{Style.RESET_ALL} 🔍 Analyze Single Claim")
            print(f"{Fore.GREEN}2.{Style.RESET_ALL} 🧪 Run Scenario Tests")
            print(f"{Fore.GREEN}3.{Style.RESET_ALL} 📊 Policy Intelligence")
            print(f"{Fore.GREEN}4.{Style.RESET_ALL} 🎲 Quick Test Scenarios")
            print(f"{Fore.GREEN}5.{Style.RESET_ALL} 📈 System Analytics")
            print(f"{Fore.GREEN}6.{Style.RESET_ALL} 💾 Export Session Log")
            print(f"{Fore.GREEN}7.{Style.RESET_ALL} 🚪 Exit")

            try:
                choice = input(f"\n{Fore.CYAN}Select option (1-7): {Style.RESET_ALL}").strip()

                if choice == "1":
                    self.analyze_single_claim()
                elif choice == "2":
                    self.run_scenario_tests()
                elif choice == "3":
                    self.policy_intelligence()
                elif choice == "4":
                    self.quick_test_scenarios()
                elif choice == "5":
                    self.system_analytics()
                elif choice == "6":
                    self.export_session_log()
                elif choice == "7":
                    self.shutdown_sequence()
                    break
                else:
                    print(f"{Fore.RED}❌ Invalid choice! Please select 1-7.{Style.RESET_ALL}")

            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}👋 Goodbye!{Style.RESET_ALL}")
                break

    def analyze_single_claim(self):
        """Analyze a single claim with detailed output"""
        print(f"\n{Fore.CYAN}🔍 SINGLE CLAIM ANALYZER")
        print(f"{'─'*30}{Style.RESET_ALL}")

        query = input(f"{Fore.YELLOW}📝 Enter claim details: {Style.RESET_ALL}").strip()

        if not query:
            print(f"{Fore.RED}❌ No claim entered!{Style.RESET_ALL}")
            return

        print(f"\n{Fore.BLUE}🤖 AI is analyzing your claim...{Style.RESET_ALL}")

        try:
            # Find relevant clauses
            relevant_chunks = semantic_search(query, self.all_chunks, self.embeddings, top_k=5)

            # Get sources
            relevant_indices = []
            for chunk in relevant_chunks:
                try:
                    idx = self.all_chunks.index(chunk)
                    relevant_indices.append(idx)
                except ValueError:
                    relevant_indices.append(0)

            relevant_sources = [self.document_sources[idx] for idx in relevant_indices]

            # Get AI decision
            result = ask_llm(query, relevant_chunks, relevant_sources)

            # Display results with style
            print(f"\n{Fore.MAGENTA}🎯 ANALYSIS RESULTS:")
            print(f"{'═'*50}{Style.RESET_ALL}")

            # Decision
            if result['decision'] == 'approved':
                print(f"{Back.GREEN}{Fore.WHITE} ✅ CLAIM APPROVED {Style.RESET_ALL}")
            elif result['decision'] == 'rejected':
                print(f"{Back.RED}{Fore.WHITE} ❌ CLAIM REJECTED {Style.RESET_ALL}")
            else:
                print(f"{Back.YELLOW}{Fore.BLACK} ⚠️ ANALYSIS ERROR {Style.RESET_ALL}")

            # Amount
            if result.get('amount'):
                print(f"{Fore.GREEN}💰 Eligible Amount: ₹{result['amount']:,}{Style.RESET_ALL}")

            # Justification
            print(f"\n{Fore.CYAN}📋 AI Justification:{Style.RESET_ALL}")
            print(f"{result['justification']}")

            # Sources
            print(f"\n{Fore.YELLOW}📄 Policy Sources Referenced:{Style.RESET_ALL}")
            unique_sources = list(set(relevant_sources))
            for source in unique_sources:
                count = relevant_sources.count(source)
                print(f"   • {source}: {count} clause(s)")

            # Log this analysis
            self.session_log.append({
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "decision": result['decision'],
                "sources": unique_sources
            })

        except Exception as e:
            print(f"{Fore.RED}❌ Analysis failed: {e}{Style.RESET_ALL}")

    def quick_test_scenarios(self):
        """Quick test with predefined scenarios"""
        print(f"\n{Fore.CYAN}🎲 QUICK TEST SCENARIOS")
        print(f"{'─'*25}{Style.RESET_ALL}")

        scenarios = [
            "19-year-old athlete, torn ACL, 3-year policy",
            "25-year-old, car accident broken ribs, 2-year policy",
            "30-year-old, emergency appendectomy, 6-month policy",
            "45-year-old, diabetes medication, 4-year policy",
            "22-year-old, mental health therapy, 3-year policy"
        ]

        print("Available scenarios:")
        for i, scenario in enumerate(scenarios, 1):
            print(f"{Fore.GREEN}{i}.{Style.RESET_ALL} {scenario}")

        try:
            choice = int(input(f"\n{Fore.CYAN}Select scenario (1-{len(scenarios)}): {Style.RESET_ALL}")) - 1
            if 0 <= choice < len(scenarios):
                print(f"\n{Fore.YELLOW}🚀 Testing: {scenarios[choice]}{Style.RESET_ALL}")

                # Analyze the selected scenario
                query = scenarios[choice]
                relevant_chunks = semantic_search(query, self.all_chunks, self.embeddings)
                relevant_indices = [self.all_chunks.index(chunk) for chunk in relevant_chunks if chunk in self.all_chunks]
                relevant_sources = [self.document_sources[idx] for idx in relevant_indices]
                result = ask_llm(query, relevant_chunks, relevant_sources)

                # Quick result display
                decision_emoji = "✅" if result['decision'] == 'approved' else "❌"
                print(f"{decision_emoji} {result['decision'].upper()}")
                print(f"📄 Sources: {', '.join(set(relevant_sources))}")

        except (ValueError, IndexError):
            print(f"{Fore.RED}❌ Invalid selection!{Style.RESET_ALL}")

    def policy_intelligence(self):
        """Show policy intelligence and insights"""
        print(f"\n{Fore.CYAN}📊 POLICY INTELLIGENCE DASHBOARD")
        print(f"{'─'*35}{Style.RESET_ALL}")

        # Policy coverage analysis
        coverage_keywords = ["surgery", "emergency", "accident", "maternity", "dental", "mental"]

        print(f"{Fore.YELLOW}🎯 Coverage Analysis:{Style.RESET_ALL}")

        for keyword in coverage_keywords:
            print(f"\n{Fore.CYAN}🔍 {keyword.title()} Coverage:{Style.RESET_ALL}")
            relevant_chunks = semantic_search(keyword, self.all_chunks, self.embeddings, top_k=2)

            if relevant_chunks:
                sources = []
                for chunk in relevant_chunks:
                    try:
                        idx = self.all_chunks.index(chunk)
                        sources.append(self.document_sources[idx])
                    except ValueError:
                        pass

                unique_sources = list(set(sources))
                if unique_sources:
                    print(f"   📄 Found in: {', '.join(unique_sources)}")
                else:
                    print(f"   ❌ No clear coverage found")
            else:
                print(f"   ❌ No coverage found")

    def system_analytics(self):
        """Display system analytics"""
        print(f"\n{Fore.CYAN}📈 SYSTEM ANALYTICS")
        print(f"{'─'*20}{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}📊 System Stats:{Style.RESET_ALL}")
        print(f"   • Total Policies: {len(self.policy_stats)}")
        print(f"   • Total Clauses: {len(self.all_chunks)}")
        print(f"   • Session Analyses: {len(self.session_log)}")

        print(f"\n{Fore.YELLOW}📋 Policy Breakdown:{Style.RESET_ALL}")
        for policy, stats in self.policy_stats.items():
            print(f"   • {policy}: {stats['clauses']} clauses")

    def export_session_log(self):
        """Export session analysis log"""
        if not self.session_log:
            print(f"{Fore.YELLOW}⚠️ No analyses in current session!{Style.RESET_ALL}")
            return

        filename = f"claims_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        try:
            with open(filename, 'w') as f:
                json.dump(self.session_log, f, indent=2)

            print(f"{Fore.GREEN}✅ Session log exported to: {filename}{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}❌ Export failed: {e}{Style.RESET_ALL}")

    def shutdown_sequence(self):
        """Cool shutdown sequence"""
        print(f"\n{Fore.CYAN}🔄 Shutting down Elite Claims Processor...{Style.RESET_ALL}")
        time.sleep(1)

        if self.session_log:
            print(f"{Fore.YELLOW}📊 Session Summary: {len(self.session_log)} claims analyzed{Style.RESET_ALL}")

        print(f"{Fore.GREEN}✅ System shutdown complete. Goodbye!{Style.RESET_ALL}")

def main():
    processor = EliteClaimsProcessor()

    if processor.startup_sequence():
        processor.main_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 System interrupted. Goodbye!{Style.RESET_ALL}")
