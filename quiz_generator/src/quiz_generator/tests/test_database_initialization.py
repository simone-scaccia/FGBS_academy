#!/usr/bin/env python
"""
Test module for Qdrant database initialization and population.
This module contains tests to verify the complete database pipeline.
"""

from random import randint
from pydantic import BaseModel
from typing import Optional
from crewai.flow import Flow, listen, start
from quiz_generator.crews.database_crew.database_crew import DatabaseCrew


class DatabaseState(BaseModel):
    provider: Optional[str] = "azure"
    certification: str = "AI_900"
    database_status: str = ""
    documents_loaded: bool = False
    success: bool = False


class DatabaseFlow(Flow[DatabaseState]):
    """Flow for testing database creation and population."""

    @start()
    def initialize_database_creation(self):
        print(f"🚀 Starting Qdrant database creation for certification: {self.state.certification}")
        print("📋 This will test the complete database pipeline...")

    @listen(initialize_database_creation)
    def create_and_populate_database(self):
        print("🔧 Running DatabaseCrew to create and populate Qdrant database...")
        try:
            result = (
                DatabaseCrew()
                .crew()
                .kickoff(inputs={"certification": self.state.certification})
            )
            
            print("✅ Database crew execution completed!")
            print(f"📊 Result: {result.raw}")
            
            self.state.database_status = "Database created and populated successfully"
            self.state.documents_loaded = True
            self.state.success = True
            
        except Exception as e:
            print(f"❌ Error during database creation: {str(e)}")
            self.state.database_status = f"Error: {str(e)}"
            self.state.success = False

    @listen(create_and_populate_database)
    def verify_database_status(self):
        if self.state.success:
            print("🎉 Database creation test completed successfully!")
            print(f"📈 Status: {self.state.database_status}")
            print(f"📚 Documents loaded: {self.state.documents_loaded}")
        else:
            print("⚠️ Database creation test failed!")
            print(f"❌ Status: {self.state.database_status}")
        
        # Save results to file for review
        with open("database_test_results.txt", "w") as f:
            f.write(f"Database Test Results\n")
            f.write(f"====================\n")
            f.write(f"Provider: {self.state.provider}\n")
            f.write(f"Certification: {self.state.certification}\n")
            f.write(f"Success: {self.state.success}\n")
            f.write(f"Status: {self.state.database_status}\n")
            f.write(f"Documents Loaded: {self.state.documents_loaded}\n")


def test_database_initialization(provider: str, certification: str):
    """
    Test the DatabaseCrew functionality with given provider and certification.
    
    Args:
        provider (str): The provider name (e.g., 'azure', 'databricks')
        certification (str): The certification name (e.g., 'AI_900')
    """
    print("🔬 Starting Qdrant Database Test...")
    print(f"📋 Provider: {provider}")
    print(f"🎓 Certification: {certification}")
    
    # Initialize the flow with custom state
    database_flow = DatabaseFlow()
    database_flow.state.provider = provider
    database_flow.state.certification = certification
    
    # Run the test
    database_flow.kickoff()
    
    return database_flow.state.success


def plot_database_flow():
    """Plot the database flow for visualization."""
    database_flow = DatabaseFlow()
    database_flow.plot()


if __name__ == "__main__":
    # Example test execution
    print("🧪 Running database initialization test...")
    
    # Test with default values
    provider = "azure"
    certification = "AI_900"
    
    success = test_database_initialization(provider, certification)
    
    if success:
        print("✅ Test completed successfully!")
    else:
        print("❌ Test failed!")
