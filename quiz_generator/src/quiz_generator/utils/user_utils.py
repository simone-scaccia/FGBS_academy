"""
User interaction utilities for Quiz Generator application.
This module contains functions for user input and data selection.
"""

import os
import re

def extract_topic_from_filename(filename):
    """
    Extract a human-readable topic name from a PDF filename.
    
    Examples:
    - 'azure-ai-services-speech-service.pdf' -> 'Speech Service'
    - 'azure-ai-foundry-foundry-local.pdf' -> 'Foundry Local'
    - 'azure-ai-services-document-intelligence-doc-intel-4.0.0.pdf' -> 'Document Intelligence'
    
    Args:
        filename (str): The PDF filename (with or without extension)
        
    Returns:
        str: Human-readable topic name
    """
    # Remove the .pdf extension if present
    base_name = filename.replace('.pdf', '')
    
    # Common patterns to extract the meaningful part
    patterns = [
        # Pattern for azure-ai-services-[topic]-[optional-parts]
        r'^azure-ai-services-(.+?)(?:-[a-z]{2,3}-\d|$)',
        # Pattern for azure-ai-[topic]-[optional-parts] 
        r'^azure-ai-(.+?)(?:-[a-z]{2,3}-\d|$)',
        # Pattern for any other azure-[something]-[topic]
        r'^azure-[^-]+-(.+?)(?:-[a-z]{2,3}-\d|$)',
        # Fallback: take everything after azure-
        r'^azure-(.+)$'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, base_name)
        if match:
            topic_part = match.group(1)
            break
    else:
        # If no pattern matches, use the whole filename
        topic_part = base_name
    
    # Clean up the topic part
    # Remove version numbers and technical suffixes
    topic_part = re.sub(r'-\d+\.\d+\.\d+.*$', '', topic_part)  # Remove version numbers
    topic_part = re.sub(r'-[a-z]{2,3}-[a-z]{2,3}.*$', '', topic_part)  # Remove technical suffixes
    
    # Convert dashes to spaces and capitalize each word
    words = topic_part.split('-')
    
    # Special handling for common abbreviations and terms
    word_mappings = {
        'ai': 'AI',
        'ml': 'ML',
        'api': 'API',
        'sdk': 'SDK',
        'cli': 'CLI',
        'luis': 'LUIS',
        'qna': 'QnA',
        'bot': 'Bot',
        'cognitive': 'Cognitive',
        'speech': 'Speech',
        'vision': 'Vision',
        'language': 'Language',
        'text': 'Text',
        'document': 'Document',
        'intelligence': 'Intelligence',
        'foundry': 'Foundry',
        'openai': 'OpenAI',
        'gpt': 'GPT'
    }
    
    # Capitalize and apply special mappings
    formatted_words = []
    for word in words:
        if word.lower() in word_mappings:
            formatted_words.append(word_mappings[word.lower()])
        else:
            formatted_words.append(word.capitalize())
    
    return ' '.join(formatted_words)

def generate_output_filenames(certification, formatted_topic):
    """
    Generate output filenames based on certification and topic to avoid overwrites.
    
    Args:
        certification (str): The certification name (e.g., 'AI_102')
        formatted_topic (str): The formatted topic name (e.g., 'Speech Service')
        
    Returns:
        dict: Dictionary with output file paths
    """
    # Create a safe filename from the topic (replace spaces and special chars)
    topic_safe = re.sub(r'[^\w\s-]', '', formatted_topic)  # Remove special chars
    topic_safe = re.sub(r'[\s_-]+', '_', topic_safe)  # Replace spaces/dashes with underscores
    topic_safe = topic_safe.strip('_').lower()  # Remove leading/trailing underscores and lowercase
    
    # Create base filename
    base_name = f"{certification}_{topic_safe}"
    
    return {
        'quiz_template': f"outputs/{base_name}_template.md",
        'questions_json': f"outputs/{base_name}_questions.json", 
        'quiz_md': f"outputs/{base_name}_quiz.md",
        'quiz_pdf': f"outputs/{base_name}_quiz.pdf",
        'completed_quiz': f"outputs/{base_name}_completed_quiz.md",
        'quiz_evaluation': f"outputs/{base_name}_evaluation.md"
    }

def get_available_providers(dataset_base_path):
    """Get list of available providers from dataset folder."""
    providers = []
    
    if os.path.exists(dataset_base_path):
        providers = [d for d in os.listdir(dataset_base_path) 
                    if os.path.isdir(os.path.join(dataset_base_path, d))]
    
    return providers

def get_available_certifications(provider, dataset_base_path):
    """Get list of available certifications for a given provider."""
    dataset_path = os.path.join(dataset_base_path, provider)
    certifications = []
    
    if os.path.exists(dataset_path):
        certifications = [d for d in os.listdir(dataset_path) 
                         if os.path.isdir(os.path.join(dataset_path, d))]
    
    return certifications

def get_available_topics(provider, certification, dataset_base_path):
    """Get list of available topics (PDF files) for a given provider and certification.
    
    Returns:
        list: List of tuples (filename_without_extension, formatted_topic_name)
    """
    dataset_path = os.path.join(dataset_base_path, provider, certification)
    topics = []
    
    if os.path.exists(dataset_path):
        pdf_files = [f for f in os.listdir(dataset_path) if f.endswith('.pdf')]
        for pdf_file in pdf_files:
            filename_without_ext = pdf_file[:-4]  # Remove .pdf extension
            formatted_topic = extract_topic_from_filename(pdf_file)
            topics.append((filename_without_ext, formatted_topic))
    
    return topics

def get_providers_with_certifications(dataset_base_path):
    """
    Get list of providers that have at least one certification available.
    
    Args:
        dataset_base_path (str): Base path to the dataset folder
        
    Returns:
        dict: Dictionary mapping provider names to their certification counts
    """
    providers_info = {}
    providers = get_available_providers(dataset_base_path)
    
    for provider in providers:
        certifications = get_available_certifications(provider, dataset_base_path)
        if certifications:  # Only include providers with certifications
            providers_info[provider] = len(certifications)
    
    return providers_info

def get_user_provider_selection(providers):
    """
    Get provider selection from user.
    
    Args:
        providers (list): List of available providers
        
    Returns:
        str or None: Selected provider or None if cancelled
    """
    print("📁 Available providers:")
    for i, provider in enumerate(providers, 1):
        print(f"  {i}. {provider}")
    
    while True:
        try:
            provider_choice = input(f"\n🔗 Select a provider (1-{len(providers)}): ").strip()
            if provider_choice.lower() in ['q', 'quit', 'exit']:
                print("\n👋 Goodbye!")
                return None
                
            provider_index = int(provider_choice) - 1
            
            if 0 <= provider_index < len(providers):
                return providers[provider_index]
            else:
                print(f"❌ Please enter a number between 1 and {len(providers)}")
        except ValueError:
            print("❌ Please enter a valid number (or 'q' to quit)")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None

def get_user_certification_selection(certifications, provider):
    """
    Get certification selection from user.
    
    Args:
        certifications (list): List of available certifications
        provider (str): Selected provider name
        
    Returns:
        str or None: Selected certification or None if cancelled
    """
    print(f"\n🎓 Available certifications for '{provider}':")
    for i, certification in enumerate(certifications, 1):
        print(f"  {i}. {certification}")
    
    while True:
        try:
            cert_choice = input(f"\n📚 Select a certification (1-{len(certifications)}): ").strip()
            cert_index = int(cert_choice) - 1
            
            if 0 <= cert_index < len(certifications):
                return certifications[cert_index]
            else:
                print(f"❌ Please enter a number between 1 and {len(certifications)}")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None

def get_user_topic_selection(topics, provider, certification):
    """
    Get topic selection from user.
    
    Args:
        topics (list): List of tuples (filename, formatted_topic)
        provider (str): Selected provider name
        certification (str): Selected certification name
        
    Returns:
        tuple or None: (filename, formatted_topic) or None if cancelled
    """
    print(f"\n📖 Available topics for '{provider}/{certification}':")
    for i, (filename, formatted_topic) in enumerate(topics, 1):
        print(f"  {i}. {formatted_topic}")
    
    while True:
        try:
            topic_choice = input(f"\n🎯 Select a topic (1-{len(topics)}): ").strip()
            topic_index = int(topic_choice) - 1
            
            if 0 <= topic_index < len(topics):
                return topics[topic_index]  # Returns (filename, formatted_topic)
            else:
                print(f"❌ Please enter a number between 1 and {len(topics)}")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None

def get_user_selections(dataset_base_path):
    """
    Get complete user selections for provider, certification, and topic.
    
    Args:
        dataset_base_path (str): Base path to the dataset folder
        
    Returns:
        tuple: (provider, certification, filename, formatted_topic) or (None, None, None, None) if cancelled
    """
    print("🎯 Welcome to Quiz Generator!")
    print("=" * 50)
    
    # Get all available providers
    providers = get_available_providers(dataset_base_path)
    
    if not providers:
        print("❌ No providers found in dataset folder!")
        return None, None, None, None
    
    # Loop until we find a valid provider with certifications
    while True:
        # Show all providers
        print("📁 Available providers:")
        for i, provider in enumerate(providers, 1):
            print(f"  {i}. {provider}")
        
        # Get provider selection
        try:
            provider_choice = input(f"\n🔗 Select a provider (1-{len(providers)}): ").strip()
            if provider_choice.lower() in ['q', 'quit', 'exit']:
                print("\n👋 Goodbye!")
                return None, None, None, None
                
            provider_index = int(provider_choice) - 1
            
            if 0 <= provider_index < len(providers):
                selected_provider = providers[provider_index]
            else:
                print(f"❌ Please enter a number between 1 and {len(providers)}")
                continue
        except ValueError:
            print("❌ Please enter a valid number (or 'q' to quit)")
            continue
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None, None, None, None
        
        # Check if selected provider has certifications
        certifications = get_available_certifications(selected_provider, dataset_base_path)
        
        if not certifications:
            print(f"❌ No certifications found for provider '{selected_provider}'!")
            print("🔄 Please select a different provider that has certifications available.")
            print()
            continue  # Go back to provider selection
        
        # If we found certifications, break out of the loop
        break
    
    # Get certification selection
    selected_certification = get_user_certification_selection(certifications, selected_provider)
    if not selected_certification:
        return None, None, None, None
    
    # Get available topics for selected certification
    topics = get_available_topics(selected_provider, selected_certification, dataset_base_path)
    
    if not topics:
        print(f"❌ No topics found for '{selected_provider}/{selected_certification}'!")
        return None, None, None, None
    
    # Get topic selection
    topic_selection = get_user_topic_selection(topics, selected_provider, selected_certification)
    if not topic_selection:
        return None, None, None, None
    
    filename, formatted_topic = topic_selection
    return selected_provider, selected_certification, filename, formatted_topic

def get_user_number_of_questions():
    """
    Get number of questions selection from user.
    
    Returns:
        int or None: Selected number of questions or None if cancelled
    """
    while True:
        try:
            num_questions_input = input("\n❓ How many questions would you like to generate? (1-5): ").strip()
            number_of_questions = int(num_questions_input)

            if number_of_questions < 1 or number_of_questions > 10:
                print("❌ Invalid number of questions. Please enter a number between 1 and 10")
            else:
                return number_of_questions
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None

def get_user_question_type_selection():
    """
    Get question type selection from user.
    
    Returns:
        str or None: Selected question type or None if cancelled
    """
    question_types = ['Multiple Choice', 'True/False', 'Short Open Question', 'Mixed']
    
    print("\n📝 Available question types:")
    for i, qtype in enumerate(question_types, 1):
        print(f"  {i}. {qtype}")
    
    while True:
        try:
            qtype_choice = input(f"\n📋 What type of questions do you want? Select a question type (1-{len(question_types)}): ").strip()
            qtype_index = int(qtype_choice) - 1
            
            if 0 <= qtype_index < len(question_types):
                return question_types[qtype_index]
            else:
                print(f"❌ Please enter a number between 1 and {len(question_types)}")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None

def get_user_choices():
    """
    Get complete user choices for number of questions and question type.
    
    Args:
        dataset_base_path (str): Base path to the dataset folder
        
    Returns:
        tuple: (number_of_questions, question_type) or (None, None) if cancelled
    """
    # Get number of questions
    number_of_questions = get_user_number_of_questions()
    if not number_of_questions:
        return None, None
    
    # Get question type
    question_type = get_user_question_type_selection()
    if not question_type:
        return None, None
    
    return number_of_questions, question_type

def display_selection_summary(provider, certification, topic, number_of_questions, question_type):
    """
    Display a summary of user selections.
    
    Args:
        provider (str): Selected provider
        certification (str): Selected certification
        topic (str): Selected topic
        number_of_questions (int): Number of questions to generate
        question_type (str): Type of questions to generate
    """
    print(f"\n🔧 You selected:")
    print(f"   Provider: {provider}")
    print(f"   Certification: {certification}")
    print(f"   Topic: {topic}")
    print(f"   Total Questions: {number_of_questions}")
    print(f"   Question's Type: {question_type}")