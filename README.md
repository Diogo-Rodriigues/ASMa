# ASMa: Theme Park Multi-Agent System

## Context and Objectives
This project implements a Multi-Agent System (MAS) to simulate a theme park environment. It was developed to explore the conception and implementation of intelligent agents capable of perceiving their environment, interpreting information, and making coordinated decisions.

**Key Goals:**
- Design a distributed MAS architecture.
- Implement intelligent agents (Visitors, Attractions, Restaurants, Manager) using the SPADE library.
- Simulate realistic behaviors such as queue management, visitor preferences (hunger, patience, budget), and park event handling.
- utilize FIPA-ACL standards for agent communication.

## Features Implemented
- **Distributed Architecture**: Managed by a central `Manager` agent with decentralized `Visitor`, `Attraction`, and `Restaurant` agents.
- **Configurable Park Layout**: The park structure (entrances, attractions, restaurants, event locations) is loaded from `ParkLayout.json`.
- **Intelligent Agents**:
    - **Manager**: Oversees park operations and events.
    - **Visitor**: Simulates guest behavior with individual attributes like budget, hunger, patience, adrenaline preference, and special needs. They navigate the park, queue for rides, and seek food.
    - **Attraction**: Manages queues, capacity, ride duration, and periodic maintenance simulations.
    - **Restaurant**: Handles food orders and capacity.
- **Agent Communication**: Uses SPADE (based on XMPP) for all inter-agent communication, employing FIPA-ACL performatives.
- **Object-Based Communication**: serialized objects (via `jsonpickle`) are exchanged instead of raw strings for complex data.

## Tech Stack
- **Language**: Python 3
- **Framework**: [SPADE](https://github.com/javipalanca/spade) (Smart Python Agent Development Environment)
- **Dependencies**: `jsonpickle` (for object serialization)
- **Communication Protocol**: XMPP (via SPADE)

## Prerequisites
- **Python 3.7+**
- **XMPP Server**: An XMPP server (like OpenFire) is required for SPADE agents to communicate.
    - *Note*: The code uses `auto_register=True`, which attempts to register agents on the server automatically. Ensure your XMPP server allows in-band registration.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd ASMa
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start your XMPP Server** (ensure it's running on `<YOUR_DOMAIN>` and with `<YOUR_PASSWORD>` configured in `main.py`).

2.  **Configure the Park**:
    - Modify `ParkLayout.json` to change attractions, restaurants, or park design.

3.  **Run the Simulation**:
    ```bash
    python main.py
    ```

    The `main.py` script will:
    - Load the park layout.
    - Start the Manager agent.
    - Initialize and start Attraction and Restaurant agents.
    - Spawn Visitor agents to enter the park.

## Project Structure

```
ASMa-GRUPO6/
├── Agents/                 # Agent implementations
│   ├── Manager.py          # Park Manager agent
│   ├── Visitor.py          # Visitor agent logic
│   ├── Attraction.py       # Attraction agent logic and queue management
│   ├── Restaurant.py       # Restaurant agent logic
│   ├── Event.py            # Event agent logic
├── Behaviours/             # SPADE Behaviours (Agent capabilities)
│   ├── Subscribe.py        # subscription handling
│   ├── VisitPark.py        # Logic for wandering and choosing activities
│   ├── SimRide.py          # Simulation of ride mechanics
│   ├── SimMaintenance.py   # Simulation of breakdowns/maintenance
│   └── ...                 # Other specific behaviours
├── Classes/                # Helper classes and Data Objects
│   ├── Coordinates.py      # Spatial logic
│   ├── VisitorData.py      # Data structure for visitor info
│   ├── Subscription.py     # Subscription data model
│   └── ...
├── main.py                 # Entry point: System initialization and orchestration
├── ParkLayout.json         # Configuration file for park entities and positions
└── requirements.txt        # Python dependencies
└── report.pdf              # Project report

```
