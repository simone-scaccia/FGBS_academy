# Application Documentation Template

**Application Owner:** Simone Scaccia, Gabriele Tromboni, Beatrice Giacobbe, Flavia De Rinaldis  
**Document Version:** v0.1  
**Reviewers:** <List of reviewers>

This documentation follows the TechOps “Application Documentation Template” for compliance and completeness.  
The documented application is **Quiz Generator (CrewAI)**, a flow that:  
1) collects user choices (provider, certification, topic, number of questions, type),  
2) generates a **template** (`template_generator_crew`),  
3) indexes certification material in **Qdrant**,  
4) generates questions with **rag_crew**,  
5) produces the final quiz with **quiz_maker_crew**.

The structure replicates the chapters and subchapters of the official template.  
Source of the template: *Application Documentation Template*. 
