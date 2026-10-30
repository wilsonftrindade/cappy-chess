# ♟️ Cappy Chess

Cappy Chess is a full-stack chess analysis application that allows players to import games, analyze moves using Stockfish, and review their performance through an interactive interface.

The application combines engine evaluations, move classifications, accuracy metrics, and game visualizations to help players identify mistakes and understand how decisions affect a game.

**[Live Application](https://capivara-chess.vercel.app)**

![Cappy Chess Game Review](docs/screenshots/game-review.png)

## Features

### Game Import

Cappy Chess supports multiple ways to import chess games:

- **Chess.com:** Retrieve recent games using a Chess.com username.
- **Lichess:** Import games directly from a Lichess account.
- **PGN:** Paste Portable Game Notation (PGN) to analyze games from any source.
- **Game Selection:** Browse imported games and select individual games for analysis.

### Stockfish-Powered Analysis

Each game is analyzed move by move using the Stockfish chess engine.

- **Position Evaluations:** Evaluate chess positions to determine which side holds the advantage.
- **Move Classification:** Classify moves based on their impact on the position and estimated winning chances.
- **Best Move Suggestions:** Compare played moves against Stockfish's recommended continuations.
- **Move Accuracy:** Calculate individual move accuracy scores based on changes in estimated win probability.
- **Win Probability Loss:** Quantify the impact of individual decisions on a player's winning chances.
- **Opening Recognition:** Identify moves that follow established opening theory using the Lichess Opening Explorer.

### Interactive Game Review

The review interface allows players to explore completed analyses through:

- **Interactive Chessboard:** Navigate through a game move by move.
- **Evaluation Bar:** Visualize which player holds the advantage.
- **Game Momentum Graph:** Track evaluation changes throughout the game and navigate to specific positions.
- **Move-by-Move Feedback:** Display move classifications, evaluations, accuracy scores, and recommended alternatives.
- **Game Summary:** Compare both players' overall accuracy and move classification statistics.

![Cappy Chess Game Summary](docs/screenshots/game-summary.png)

### Asynchronous Processing

Analyzing entire chess games with Stockfish is computationally expensive. To keep the API responsive, Cappy Chess processes game reviews asynchronously.

- **Redis Queue (RQ):** Manages background analysis jobs.
- **Dedicated Workers:** Execute Stockfish analysis independently of the API server.
- **Progress Tracking:** Allows the frontend to monitor analysis progress through polling.
- **Persistent Storage:** Saves games, review statuses, and completed analyses in PostgreSQL.

---

## Architecture

Cappy Chess separates HTTP request handling from computationally intensive chess analysis using an asynchronous job-processing architecture.

```mermaid
flowchart TD
    Client["React + TypeScript<br/>Vercel"] -->|REST API| API["FastAPI<br/>Render"]

    API -->|Game Import| External["Chess.com / Lichess APIs"]
    API <-->|Games and Reviews| DB[("PostgreSQL")]

    API -->|Enqueue Analysis| Redis[("Redis Queue")]
    Redis -->|Dequeue Jobs| Worker["RQ Background Worker"]

    Worker -->|Evaluate Positions| Stockfish["Stockfish Engine"]
    Worker -->|Opening Book Lookup| Explorer["Lichess Opening Explorer"]
    Worker -->|Persist Results| DB

    Client -->|Poll Review Progress| API
```

### Review Pipeline

1. **Import:** The user imports a game from Chess.com, Lichess, or PGN.
2. **Submission:** The frontend sends the selected game to FastAPI for analysis.
3. **Job Creation:** FastAPI creates a review record in PostgreSQL and enqueues a background job in Redis.
4. **Engine Analysis:** An RQ worker retrieves the job and analyzes the game using Stockfish.
5. **Classification:** Engine evaluations are processed to calculate win probability loss, move accuracy, and classifications. Opening-book moves are identified separately.
6. **Game Summary:** Individual move results are aggregated into player accuracy scores and classification statistics.
7. **Persistence:** The completed review is stored in PostgreSQL.
8. **Retrieval:** The frontend polls the API for progress and retrieves the completed analysis.

---

## Tech Stack

| Component | Technologies |
|---|---|
| **Frontend** | React, TypeScript, Vite |
| **Backend** | Python, FastAPI |
| **Chess Engine** | Stockfish, python-chess |
| **Database** | PostgreSQL, SQLAlchemy |
| **Background Processing** | Redis, RQ |
| **Containerization** | Docker |
| **Deployment** | Vercel, Render |

---

## Analysis Methodology (V1)

Cappy Chess implements custom move classification and accuracy algorithms using Stockfish evaluations.

The current implementation is **Version 1** of the analysis system. Its goal is to provide meaningful feedback through interpretable metrics and classifications, rather than reproduce the exact proprietary algorithms used by platforms such as Chess.com.

### 1. Position Evaluation and Win Probability

For each move, Stockfish analyzes the position before and after the move, returning centipawn evaluations, mate scores, and the engine's preferred continuation.

Centipawn evaluations are converted into estimated win probabilities using a logistic function:

```math
P_{\text{white}}(cp) = \frac{1}{1 + e^{-0.00368208 \cdot cp}}
```


Here, `cp` represents the centipawn evaluation from White's perspective.

Black's estimated win probability is calculated as:

```math
P_{\text{black}} = 1 - P_{\text{white}}
```


Forced mate evaluations are handled separately, assigning a probability of 1 or 0 depending on whether the player has a forced mate or is being mated.

This conversion makes it possible to measure the impact of moves in terms of estimated winning chances rather than relying exclusively on raw centipawn differences.

### 2. Win Probability Loss

**Win Probability Loss (WPL)** measures how much a move reduces the player's estimated winning chances.

For each move:

```math
WPL = \max(0, P_{\text{before}} - P_{\text{after}})
```


Both probabilities are calculated from the perspective of the player making the move.

This approach helps account for the fact that identical centipawn losses can have different practical significance depending on the position.

### 3. Move Classification

Moves are classified primarily according to their win probability loss.

The current V1 thresholds are:

| Classification | Win Probability Loss |
|---|---|
| **Best** | Stockfish's top move, or zero calculated WPL |
| **Excellent** | Less than 2 percentage points |
| **Good** | 2–5 percentage points |
| **Inaccuracy** | 5–10 percentage points |
| **Mistake** | 10–20 percentage points |
| **Blunder** | 20 percentage points or more |

**Mate-specific classification:** Forced mate scenarios receive additional treatment, considering whether a move creates, preserves, loses, or changes the distance to a forced mate, rather than relying exclusively on probability loss.

**Opening-book classification:** Book moves are detected using the Lichess Opening Explorer. A move is classified as a book move if it appears in at least 20 games and represents at least 1% of the recorded moves from that position, using the configured opening database filters.

Opening-book classification continues until the first move that fails these criteria.

The current implementation supports seven classifications: **Book, Best, Excellent, Good, Inaccuracy, Mistake, and Blunder**.

More specialized classifications, such as Brilliant, Great, and Miss, are potential additions for future versions.

### 4. Individual Move Accuracy

Each move receives an accuracy score between 0 and 100, derived from its win probability loss.

Cappy Chess uses an exponential decay function to transform probability loss into move accuracy:

```math
A_{\text{move}} =
\min\left(
100,\ 
\max\left(
0,\ 
103.16681 e^{-0.04354415(100 \cdot WPL)} - 2.16692
\right)
\right)
```


### 5. Overall Game Accuracy

Overall game accuracy is calculated separately for White and Black.

Rather than taking a simple arithmetic mean of individual move accuracies, Cappy Chess combines two complementary measures:

**A. Severity-Weighted Accuracy**

Individual move accuracies are averaged using weights that increase as accuracy decreases.

This gives particularly poor moves greater influence on the final score, reflecting the disproportionate impact that major mistakes can have on a chess game.

**B. Volatility-Weighted Accuracy**

The second component considers the volatility of estimated winning probabilities throughout the game.

- A rolling window measures changes in estimated win probability.
- Positions with greater volatility receive higher weights.
- A weighted root-mean-square calculation of move accuracy losses penalizes large mistakes more heavily than small inaccuracies.

This component gives additional importance to moves made during volatile or critical phases of a game.

The final game accuracy is:

```math
A_{\text{game}} =
0.5 \cdot A_{\text{severity}}
+
0.5 \cdot A_{\text{volatility}}
```


Both components contribute equally to the final score.

**Book moves are excluded from the overall accuracy calculation**, allowing the score to focus on decisions made outside the recognized opening sequence.

### V1 Limitations and Future Refinements

The analysis methodology is an initial implementation with custom thresholds and weighting functions.

Current limitations include:

- Move classification thresholds are heuristic and may require further calibration.
- Special classifications, including Brilliant, Great, and Miss, are not yet supported.
- Results may differ from Chess.com or Lichess because of differences in engine settings, evaluation models, and classification methodology.

Future iterations will focus on refining these algorithms, improving edge-case handling, and introducing additional classifications.

---

## Local Development

### Prerequisites

- Docker and Docker Compose
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/wilsonftrindade/chess-coach.git
cd chess-coach
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
POSTGRES_PASSWORD=your_local_password
DATABASE_URL=postgresql+psycopg://chess_coach:your_local_password@postgres:5432/chess_coach
REDIS_URL=redis://redis:6379/0
LICHESS_API_TOKEN=your_lichess_api_token
```

Replace the placeholders with your own credentials. The PostgreSQL password in `DATABASE_URL` must match `POSTGRES_PASSWORD`.

Create `frontend/.env.local`:

```env
VITE_API_URL=http://localhost:8000
```

### 3. Start Backend Services

From the repository root:

```bash
docker compose up -d --build
```

Docker Compose starts:

- FastAPI backend
- PostgreSQL database
- Redis instance
- RQ background worker

Apply the database migrations:

```bash
docker compose exec backend alembic upgrade head
```

The backend should be available at:

- **API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health

### 4. Start the Frontend

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** to access Cappy Chess.

---

## Future Improvements

- **Real-Time Progress:** Replace frontend polling with Server-Sent Events (SSE).
- **Analysis Refinement:** Improve classification thresholds, accuracy calculations, and mate-scenario handling.
- **Additional Classifications:** Implement specialized categories such as Brilliant, Great, and Miss.
- **Deeper Insights:** Expand game statistics and identify recurring patterns in player performance.
- **User Experience:** Improve mobile responsiveness and analysis visualizations
