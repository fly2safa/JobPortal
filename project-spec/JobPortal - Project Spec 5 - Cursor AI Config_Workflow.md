# Cursor AI Config : Workflow
	Configure a structured workflow in Cursor IDE to manage project setup, feature development, testing, and deployment efficiently, using AI-assisted suggestions, rules, and contextual navigation.

1. ** Workflow Using Command Prompts **

Cursor IDE Command Prompts for Job Portal

New Projects

	Define Project Requirements Document
	
		Use @doc to reference PRD and project design notes.


	Define Project Structure

		Backend: models, repositories, services, routers, db

		Frontend: app, components, features, hooks, store

		Docker: backend Dockerfile, frontend Dockerfile, docker-compose.yml

		Config: .env, settings.py, tailwind.config.js



Building Features

	Implementation Plan for a Feature

		Use Cursor AI "Ask" or "Agent" to generate high-level implementation plan


	Review the Implementation Plan

		Validate tasks, dependencies, and folder structure


	Select Files and Implement

		Navigate using @Files, @Folders, @Code

		Use @CursorRules to enforce coding standards


	UI/UX Guidelines

		Reference design files using @Docs

		Suggest CSS/Tailwind classes using Cursor AI


	Manually Test the Feature

		Backend: test APIs via Swagger docs or Postman

		Frontend: test UI components in browser


	Commit and Merge

		Use Cursor AI to suggest descriptive commit messages

		Ensure feature branch merged to main

		
2. ** Recommended Cursor Workflow Prompts **
Cursor IDE supports workflow prompts to automate or guide repetitive tasks. Here’s how to configure them:

** A. New Project Setup Prompt **

	Trigger: “Initialize Job Portal Project”


	Actions:

		Create folder structure

		Generate main.py, Dockerfile, docker-compose.yml

		Add default .env placeholders

		Link PRD using @doc



** B. Feature Implementation Prompt **

	Trigger: “Build Feature <feature_name>”

	Actions:

		Create models, services, and routes if backend feature

		Create components, hooks, and API services if frontend

		Apply UI/UX guidelines via @Docs or Tailwind suggestions

		Suggest unit tests template



** C. Code Review Prompt **

	Trigger: “Review Code”

	Actions:

		Validate Cursor rules (naming conventions, model registration)

		Suggest optimizations (async calls, Tailwind classes)

		Highlight missing environment variables or Docker mappings



** D. Deployment Preparation Prompt **

	Trigger: “Prepare for Docker Deployment”

	Actions:

		Verify Dockerfiles

		Check docker-compose.yml for correct env variables

	Suggest health checks for containers

	Prepare startup scripts
	
	

3. ** Cursor Rules Integration **

	Example Rules for Job Portal:

		1.
			Model Registration Rule: Every Beanie model must be added to init_db.py.

		2.
			Environment Rule: .env must contain MONGODB_URI, DATABASE_NAME, SECRET_KEY, NEXT_PUBLIC_API_URL.

		3.
			Frontend Component Rule: All React components must have proper Tailwind classnames for padding, margin, colors, and responsive design.

		4.
			Commit Rule: Commit messages must include feature name and JIRA/task ID if applicable.



4. ** Cursor AI Best Practices for Workflow **

	Use “Ask” model for quick code snippets or validation.

	Use “Agent” model for multi-step feature creation across backend and frontend.

	Use @Files, @Folders, @Code, and @Docs extensively to maintain context.

	Maintain a feature-based folder organization for scalability.

	Regularly update Cursor rules to reflect coding standards and project-specific guidelines.