#!/usr/bin/env python3
"""
Final Test - Clean Enhanced Insurance Claims System
"""

from clean_enhanced_system import CleanEnhancedSystem
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

def main():
    """Run the final enhanced system"""
    print(f"{Back.GREEN}{Fore.WHITE}{Style.BRIGHT}")
    print("🏥 FINAL ENHANCED INSURANCE CLAIMS SYSTEM")
    print("=========================================")
    print("✅ Real policy data from PDF")
    print("✅ Gemini web search for hospitals")
    print("✅ Emergency contacts & care tips")
    print("✅ Hospitality assistance")
    print(f"{Style.RESET_ALL}")

    # Initialize system
    system = CleanEnhancedSystem()

    # Load documents
    if not system.load_documents("docs"):
        print(f"{Fore.RED}❌ Failed to load documents")
        return

    print(f"\n{Fore.GREEN}🚀 System ready!")

    # Show sample queries
    samples = [
        "knee surgery in Pune, 3 month policy",
        "heart attack emergency in Mumbai, 6 month policy",
        "accident fracture in Delhi, 1 month policy"
    ]

    print(f"\n{Fore.CYAN}📝 Sample queries:")
    for i, sample in enumerate(samples, 1):
        print(f"   {i}. {sample}")

    # Interactive mode
    print(f"\n{Fore.YELLOW}💬 Interactive Mode:")
    print("• Enter insurance claims")
    print("• Type 'help' for general assistance")
    print("• Type 'quit' to exit")

    while True:
        try:
            user_input = input(f"\n{Fore.CYAN}Your query: {Fore.WHITE}")

            if user_input.lower() in ['quit', 'exit', 'q']:
                print(f"{Fore.GREEN}👋 Thank you for using the Enhanced Claims System!")
                break

            elif user_input.lower() in ['help', 'hospitality']:
                help_mode(system)
                continue

            if user_input.strip():
                result = system.process_claim_query(user_input)
                display_clean_result(result)
            else:
                print(f"{Fore.YELLOW}Please enter a query.")

        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}👋 Goodbye!")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {str(e)}")

def display_clean_result(result):
    """Display result in clean, concise format"""
    print(f"\n{Back.BLUE}{Fore.WHITE} 📋 CLAIM ANALYSIS {Style.RESET_ALL}")

    # Decision with color
    decision = result['decision']
    if decision == 'approved':
        print(f"{Fore.GREEN}✅ APPROVED")
    elif decision == 'rejected':
        print(f"{Fore.RED}❌ REJECTED")
    else:
        print(f"{Fore.YELLOW}⚠️ REVIEW NEEDED")

    # Location
    location = result.get('location_detected')
    if location and location != 'Not specified':
        print(f"📍 {location}")

    # Brief explanation
    explanation = result.get('user_friendly_explanation', '')
    if explanation:
        print(f"\n💬 {explanation}")

    # Emergency flag
    if result.get('emergency_override'):
        print(f"\n{Fore.RED}🚨 Emergency fast-track applied")

    # Healthcare section
    print(f"\n{Back.GREEN}{Fore.WHITE} 🏥 IMMEDIATE ASSISTANCE {Style.RESET_ALL}")

    # Hospitals (max 3, concise)
    hospitals = result.get('nearby_hospitals', [])
    if hospitals:
        print(f"\n🏥 Nearby hospitals:")
        for i, hospital in enumerate(hospitals[:3], 1):
            print(f"   {i}. {hospital}")

    # Emergency contacts (max 3)
    contacts = result.get('emergency_contacts', [])
    if contacts:
        print(f"\n📞 Emergency:")
        for contact in contacts[:3]:
            print(f"   • {contact}")

    # Care tips (max 3, practical)
    tips = result.get('immediate_care_tips', [])
    if tips:
        print(f"\n💡 Immediate care:")
        for i, tip in enumerate(tips[:3], 1):
            print(f"   {i}. {tip}")

    # Specialist
    specialist = result.get('specialist_recommendation')
    if specialist:
        print(f"\n👨‍⚕️ See: {specialist}")

    print(f"\n{'-'*50}")

def help_mode(system):
    """Hospitality assistance mode"""
    print(f"\n{Back.CYAN}{Fore.WHITE} 🏨 HOSPITALITY ASSISTANT {Style.RESET_ALL}")
    print("Ask about hospitals, travel, emergency services, etc.")
    print("(Type 'back' to return)")

    while True:
        question = input(f"\n{Fore.CYAN}Question: {Fore.WHITE}")

        if question.lower() in ['back', 'return', 'exit']:
            break

        if question.strip():
            print(f"\n{Fore.YELLOW}🔍 Searching...")
            answer = system.hospitality_assistant(question)
            print(f"\n{Fore.GREEN}🏨 {answer}")
        else:
            print(f"{Fore.YELLOW}Please ask a question.")

if __name__ == "__main__":
    main()
