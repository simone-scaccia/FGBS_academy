"""
User interaction utilities for Quiz Generator application.
This module contains functions for user input and data selection.
"""

import os

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
    """Get list of available topics (PDF files) for a given provider and certification."""
    dataset_path = os.path.join(dataset_base_path, provider, certification)
    topics = []
    
    if os.path.exists(dataset_path):
        topics = [f[:-4] for f in os.listdir(dataset_path) 
                 if f.endswith('.pdf')]
    
    return topics

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
            provider_index = int(provider_choice) - 1
            
            if 0 <= provider_index < len(providers):
                return providers[provider_index]
            else:
                print(f"❌ Please enter a number between 1 and {len(providers)}")
        except ValueError:
            print("❌ Please enter a valid number")
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
        topics (list): List of available topics
        provider (str): Selected provider name
        certification (str): Selected certification name
        
    Returns:
        str or None: Selected topic or None if cancelled
    """
    print(f"\n📖 Available topics for '{provider}/{certification}':")
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")
    
    while True:
        try:
            topic_choice = input(f"\n🎯 Select a topic (1-{len(topics)}): ").strip()
            topic_index = int(topic_choice) - 1
            
            if 0 <= topic_index < len(topics):
                return topics[topic_index]
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
        tuple: (provider, certification, topic) or (None, None, None) if cancelled
    """
    print("🎯 Welcome to Quiz Generator!")
    print("=" * 50)
    
    # Get available providers
    providers = get_available_providers(dataset_base_path)
    
    if not providers:
        print("❌ No providers found in dataset folder!")
        return None, None, None
    
    # Get provider selection
    selected_provider = get_user_provider_selection(providers)
    if not selected_provider:
        return None, None, None
    
    # Get available certifications for selected provider
    certifications = get_available_certifications(selected_provider, dataset_base_path)
    
    if not certifications:
        print(f"❌ No certifications found for provider '{selected_provider}'!")
        return None, None, None
    
    # Get certification selection
    selected_certification = get_user_certification_selection(certifications, selected_provider)
    if not selected_certification:
        return None, None, None
    
    # Get available topics for selected certification
    topics = get_available_topics(selected_provider, selected_certification, dataset_base_path)
    
    if not topics:
        print(f"❌ No topics found for '{selected_provider}/{selected_certification}'!")
        return None, None, None
    
    # Get topic selection
    selected_topic = get_user_topic_selection(topics, selected_provider, selected_certification)
    if not selected_topic:
        return None, None, None
    
    return selected_provider, selected_certification, selected_topic

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

            if number_of_questions < 1 or number_of_questions > 5:
                print("❌ Invalid number of questions.Please enter a number between 1 and 5")
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

def get_user_choices(dataset_base_path):
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