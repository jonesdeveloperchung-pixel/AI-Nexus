from typing import Dict, Optional

class PromptManager:
    def __init__(self):
        # For MVP, prompts are stored in-memory.
        # In a production system, this would be backed by a secure database.
        self._prompts: Dict[str, Dict[str, str]] = {}
        self._initialize_default_prompts()

    def _initialize_default_prompts(self):
        # Default prompts for demonstration
        self.add_prompt(
            course_id="default",
            system_message="You are a helpful assistant.",
            user_message_template="The user asks: {user_query}"
        )
        self.add_prompt(
            course_id="math101",
            system_message="You are a math tutor for Math 101. Provide clear explanations and step-by-step solutions.",
            user_message_template="The student asks: {user_query}. Please help them understand this concept."
        )
        self.add_prompt(
            course_id="history202",
            system_message="You are a history expert for History 202. Focus on historical facts and context.",
            user_message_template="The student asks about a historical event: {user_query}. Provide a concise summary."
        )

    def add_prompt(self, course_id: str, system_message: str, user_message_template: str):
        """
        Adds or updates a prompt for a given course_id.
        In a real system, this would be admin-only and potentially encrypted.
        """
        self._prompts[course_id] = {
            "system_message": system_message,
            "user_message_template": user_message_template
        }
        print(f"Prompt for course '{course_id}' added/updated.")

    def get_prompt(self, course_id: str) -> Optional[Dict[str, str]]:
        """
        Retrieves the prompt for a given course_id.
        """
        return self._prompts.get(course_id)

    def get_all_prompts(self) -> Dict[str, Dict[str, str]]:
        """
        Retrieves all stored prompts.
        """
        return self._prompts

if __name__ == "__main__":
    manager = PromptManager()

    print("All initial prompts:")
    for course_id, prompt in manager.get_all_prompts().items():
        print(f"  Course ID: {course_id}")
        print(f"    System: {prompt['system_message']}")
        print(f"    User Template: {prompt['user_message_template']}")

    # Test retrieving a specific prompt
    math_prompt = manager.get_prompt("math101")
    if math_prompt:
        print("\nMath 101 Prompt:")
        print(f"  System: {math_prompt['system_message']}")
        print(f"  User Template: {math_prompt['user_message_template']}")

    # Test updating a prompt
    manager.add_prompt(
        course_id="math101",
        system_message="You are an advanced math tutor for Math 101. Focus on problem-solving strategies.",
        user_message_template="The student needs help with: {user_query}. Guide them through the solution."
    )
    updated_math_prompt = manager.get_prompt("math101")
    if updated_math_prompt:
        print("\nUpdated Math 101 Prompt:")
        print(f"  System: {updated_math_prompt['system_message']}")
        print(f"  User Template: {updated_math_prompt['user_message_template']}")

    # Test a non-existent prompt
    non_existent_prompt = manager.get_prompt("nonexistent")
    print(f"\nNon-existent prompt: {non_existent_prompt}")
