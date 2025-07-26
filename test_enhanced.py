#!/usr/bin/env python3
"""
Test script for the Enhanced Claims System
"""

from enhanced_system import EnhancedClaimsSystem
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

def main():
    """Test the enhanced claims system"""
    print(f"{Back.GREEN}{Fore.WHITE}{Style.BRIGHT}")
    print("🏥 ENHANCED INSURANCE CLAIMS SYSTEM TEST")
    print("========================================")
    print("Real policy data + Gemini web search")
    print(f"{Style.RESET_ALL}")

    # Initialize the enhanced system
    system = EnhancedClaimsSystem()

    # Load documents
    if not system.load_documents("docs"):
        print(f"{Fore.RED}❌ Failed to load documents")
        return

    print(f"\n{Fore.GREEN}🚀 System ready!")

    # Interactive mode
    print(f"\n{Fore.CYAN}💬 Enter your claim queries (type 'quit' to exit, 'help' for assistance):")

    while True:
        try:
            user_input = input(f"\n{Fore.CYAN}Your query: {Fore.WHITE}")

            if user_input.lower() in ['quit', 'exit', 'q']:
                print(f"{Fore.GREEN}👋 Thank you!")
                break

            elif user_input.lower() in ['help', 'hospitality']:
                provide_help(system)
                continue

            if user_input.strip():
                print(f"\n{Fore.YELLOW}🔄 Processing...")
                result = system.process_claim_query(user_input)
                display_result(result)
            else:
                print(f"{Fore.YELLOW}Please enter a valid query.")

        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}👋 Goodbye!")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {str(e)}")

def display_result(result):
    """Display claim result in a clean format"""
    print(f"\n{Back.BLUE}{Fore.WHITE} 📋 CLAIM ANALYSIS RESULT {Style.RESET_ALL}")

    # Decision
    if result['decision'] == 'approved':
        print(f"{Fore.GREEN}✅ APPROVED")
    elif result['decision'] == 'rejected':
        print(f"{Fore.RED}❌ REJECTED")
    else:
        print(f"{Fore.YELLOW}⚠️ ERROR")

    # Location
    if result.get('location_detected') and result['location_detected'] != 'Not specified':
        print(f"📍 Location: {result['location_detected']}")

    # Explanation
    print(f"\n💬 {result.get('user_friendly_explanation', 'No explanation')}")

    # Emergency
    if result.get('emergency_override'):
        print(f"\n{Fore.RED}🚨 Emergency fast-track applied!")

    # Healthcare assistance
    print(f"\n{Back.GREEN}{Fore.WHITE} 🏥 HEALTHCARE ASSISTANCE {Style.RESET_ALL}")

    # Hospitals
    if result.get('nearby_hospitals'):
        print(f"\n🏥 Recommended hospitals:")
        for i, hospital in enumerate(result['nearby_hospitals'][:3], 1):
            print(f"   {i}. {hospital}")

    # Emergency contacts
    if result.get('emergency_contacts'):
        print(f"\n📞 Emergency contacts:")
        for contact in result['emergency_contacts'][:3]:
            print(f"   • {contact}")

    # Care tips
    if result.get('immediate_care_tips'):
        print(f"\n💡 Immediate care tips:")
        for i, tip in enumerate(result['immediate_care_tips'][:3], 1):
            print(f"   {i}. {tip}")

    # Specialist
    if result.get('specialist_recommendation'):
        print(f"\n👨‍⚕️ Specialist needed: {result['specialist_recommendation']}")

    print(f"\n{'-'*50}")

def provide_help(system):
    """Provide general help using Gemini"""
    print(f"\n{Back.CYAN}{Fore.WHITE} 🏨 HOSPITALITY ASSISTANT {Style.RESET_ALL}")
    print("Ask me about hospitals, emergency services, travel assistance, etc.")

    while True:
        question = input(f"\n{Fore.CYAN}Your question (or 'back'): {Fore.WHITE}")

        if question.lower() in ['back', 'return']:
            break

        if question.strip():
            try:
                response = system.llm.generate_content(f"""
                You are a helpful hospitality assistant in India. Provide accurate, concise information about:

                Question: {question}

                Give practical, helpful information in 2-3 sentences.
                """)

                print(f"\n{Fore.GREEN}🏨 {response.text}")

            except Exception as e:
                print(f"{Fore.RED}❌ Sorry, couldn't process that: {str(e)}")

if __name__ == "__main__":
    main()
