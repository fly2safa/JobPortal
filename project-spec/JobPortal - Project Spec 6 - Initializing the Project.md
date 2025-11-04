# Initializing the Project


** Backend (FastAPI + Beanie + MongoDB) **

The backend is built using FastAPI, a modern, high-performance Python framework ideal for asynchronous APIs. Beanie is used as the ODM (Object Document Mapper) for MongoDB, providing async operations, schema validation, and automatic collection creation.

Key aspects:

	** Virtual Environment Management: ** Isolated Python environment using venv ensures dependency management and avoids conflicts.


	** Dependency Management: ** All required packages are installed via requirements.txt, including FastAPI, Uvicorn (ASGI server), Beanie, Motor (MongoDB async driver), Pydantic, Passlib, and JWT libraries.

	** Environment Configuration: ** Sensitive information like database URI and secret keys are managed through .env files, ensuring security and ease of configuration.

	** Folder Structure: ** Organized into models, schemas, services, routers, db, and core to maintain separation of concerns and enforce clean architecture.

	** Initialization: ** main.py and init_db.py ensure proper startup, database connection, and model registration.

	** Testing: ** Swagger UI (/docs) provides interactive API documentation for testing endpoints during development.



** Frontend (Next.js + Tailwind CSS)** 

The frontend is built with Next.js using the App Router pattern, providing a modular, feature-based architecture that is ideal for enterprise applications. Tailwind CSS ensures consistent styling, responsive design, and rapid UI development.

Key aspects:

	** Project Structure: ** Organized into app (pages/routes), components (reusable UI elements), features (feature-specific components and hooks), hooks (global React hooks), lib (utilities), store (state management), styles, and public (static assets).

	** Tailwind Integration: ** Provides utility-first CSS, enabling rapid design with responsive and consistent styling for buttons, forms, cards, and layouts.

	** TypeScript/JSX Support: ** Ensures type safety, better developer experience, and maintainable code.

	** Development Workflow: ** npm run dev launches the app in development mode with hot-reloading.

	** Scalable Component Design: ** Modular feature-based architecture allows independent development of auth, dashboard, and job listings.



# Instructions

1. ** Backend – FastAPI + Beanie **

** Step 1: Navigate to backend **
	cd backend 

** Step 2: Set Up Python Virtual Environment **
	python -m venv venv

		Activate virtual environment:

			** Windows: ** venv\Scripts\activate

			** Linux/Mac: ** source venv/bin/activate



** Step 3: Install Dependencies **
	1. Create requirements.txt:

		fastapi uvicorn beanie motor pydantic python-jose passlib[bcrypt]

	2. Install packages:

		pip install -r requirements.txt


 
2. ** Frontend – Next.js + Tailwind CSS **

	** Step 1: Create Frontend Folder **
		cd ../ npx create-next-app@latest frontend

			Choose App Router and JSX.

			Navigate to frontend/ folder.



	** Step 2: Install Tailwind CSS **
		npm install -D tailwindcss postcss autoprefixer npx tailwindcss init -p
 


# Notes
	Always activate Python virtual environment before installing or running backend.

	Keep .env secure; use .env.example for team sharing.