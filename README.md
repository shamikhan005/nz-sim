# nz-sim: net zero scenario auditor

a mathematically grounded, multi-agent AI pipeline designed to audit corporate sustainability claims, detect carbon leakage, and simulate mathematically sound decarbonization strategies.

## the problem & solution

standard LLMs hallucinate math, making them fundamentally unsafe to strict carbon accounting and environmental auditing.

**nz-sim** solves this by decoupling computation from probabilistic reasoning.

instead of asking an AI to do math, nz-sim anchors all data to a **deterministic python engine** that calculates the true physical carbon baseline. it then passes that unalterable truth into a chain of **five K2-Think-v2 AI agents**. these agents acts as a corporate auditing board detecting logical inconsistencies, finding supply chain leaks, and challening public net-zero claims against simulated mathemtical realities.

## architecture

<img width="638" height="877" alt="Screenshot 2026-02-16 023834" src="https://github.com/user-attachments/assets/df77db43-baa4-4d2b-bb9d-cf9aaf1cde90" />

1. **the math anchor (no AI):** hard-calculates true scope 1 & 2 emissions based on user inputs (*kwh x emission_factor*) to establish a deterministic baseline.

2. **agent 1 (the auditor):** compares reported emissions against the math engine to flag impossible claims.

3. **agent 2 (the investigator):** scans for carbon leakage, scope 3 omissions, and boundary manipulations.

4. **agent 3 (the simulator):** generates 3 strict counterfactual pathways (grid shift, transport efficiency, offsets) using constrained math rules.

5. **agent 4 (the strategist):** stress-tests the user's public claim against the simulations to issue a reality check verdict.

6. **agent 5 (the synthesizer):** strips out AI thought-loops and synthesizes the complex JSON output into a highly scannable C-suite executive briefing.

## tech stack

* **AI model:** MBZUAI-IFM/K2-Think-v2
* **Backend:** FastAPI, Python, uv package manager
* **Frontend:** Next.js (App Router), TypeScript, Tailwind CSS
* **Data Visualization:** Recharts

## local development

**1. clone the repository**

```bash
git clone https://github.com/shamikhan005/nz-sim.git
cd nz-sim
```

**2. set up the FastAPI backend**

```bash
# create .env file in the root directory
echo "K2_API_KEY=your_api_key_here" > .env

# install dependencies using uv
uv sync

# run fastAPI server
uv run uvicorn app.main:app --reload
```

the backend will now be running on ```http://127.0.0.1:8000```

**3. set up the Next.js frontend**

```bash
cd frontend

# install node dependencies
npm install

# start the Next.js development server
npm run dev
```

the frontend will now be running on ```http://localhost:3000```
