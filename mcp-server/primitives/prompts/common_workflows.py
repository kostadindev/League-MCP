"""Common workflow prompts for League of Legends API usage."""

import logging
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)


def register_workflow_prompts(mcp: FastMCP):
    """Register all workflow prompts."""
    
    @mcp.prompt(name="find_player_stats", description="Complete workflow to find a player's statistics")
    async def find_player_stats_prompt(game_name: str = "Player", tag_line: str = "NA1", region: str = "na1") -> str:
        """Generate a complete workflow to find and analyze a player's statistics."""
        logger.info(f"Prompt called: find_player_stats_prompt")
        
        prompt = f"""
# Complete Player Analysis Workflow

You are analyzing League of Legends player: **{game_name}#{tag_line}** in region **{region.upper()}**

## Step-by-Step Analysis Process:

### 1. Player Identification
- Use `get_account_by_riot_id` with game_name="{game_name}" and tag_line="{tag_line}"
- Extract the PUUID for subsequent API calls

### 2. Summoner Profile  
- Use `get_summoner_by_puuid` with the PUUID from step 1
- Record summoner level, profile icon, last update time

### 3. Ranked Information
- Use `get_league_entries_by_summoner` with the summonerID
- Report current tier, division, LP, wins/losses for each queue

### 4. Recent Match History
- Use `get_match_ids_by_puuid` to get recent match IDs (last 10 matches)
- For each match, use `get_match_details` to get comprehensive match data
- Calculate performance metrics and trends

### 5. Champion Mastery
- Use `get_champion_masteries_by_puuid` to see top mastery champions
- Cross-reference with recent match performance

Present your analysis in a structured report with actionable insights.
"""
        
        return prompt

    @mcp.prompt(name="tournament_setup", description="Complete tournament organization workflow")
    async def tournament_setup_prompt(tournament_name: str = "My Tournament", region: str = "na1") -> str:
        """Generate a complete workflow for setting up a League of Legends tournament."""
        logger.info(f"Prompt called: tournament_setup_prompt")
        
        prompt = f"""
# Complete Tournament Setup Workflow

You are organizing: **{tournament_name}** in region **{region.upper()}**

## Prerequisites:
- Production API Key required
- Tournament organizer verification from Riot
- Valid callback URL for receiving match results

## Setup Steps:
1. Use `create_tournament_provider` with region and callback URL
2. Use `create_tournament` with provider_id and tournament name  
3. Use `generate_tournament_codes` for matches
4. Set up callback handling for match results
5. Use `get_tournament_lobby_events` to monitor matches

## Compliance Requirements:
- Allocate 70%+ of entry fees to prize pool
- Minimum 20 participants
- Transparent win conditions
- No gambling elements

Follow Riot's tournament policies throughout the process.
"""
        
        return prompt

    @mcp.prompt(name="champion_analysis", description="Deep dive analysis of a specific champion")
    async def champion_analysis_prompt(champion_name: str = "Azir", region: str = "na1") -> str:
        """Generate a comprehensive champion analysis workflow.
        
        Args:
            champion_name: The champion to analyze
            region: Region for statistics
        """
        logger.info(f"Prompt called: champion_analysis_prompt(champion_name={champion_name})")
        
        prompt = f"""
# Comprehensive Champion Analysis: {champion_name}

You are conducting a deep analysis of **{champion_name}** in the **{region.upper()}** region.

## Data Collection Strategy:

### 1. Champion Static Data
Gather champion information from Data Dragon:
- Use Data Dragon resources to get {champion_name}'s:
  - Base statistics and scaling
  - Ability descriptions and damage values
  - Recommended items and builds
  - Lore and thematic information
  - Available skins and chromas

### 2. Meta Analysis
Analyze current meta position:
- Check recent patch notes for {champion_name} changes
- Identify current build paths and rune setups
- Compare pick/ban rates across different ranks
- Assess role flexibility (primary/secondary positions)

### 3. High-Level Performance Data
Collect data from skilled players:
- Use `get_challenge_leaderboard` to find top {champion_name} players
- Analyze master+ player match histories
- Look for common build patterns and gameplay strategies
- Identify successful {champion_name} one-tricks

### 4. Match Analysis
Deep dive into recent matches:
- Find recent ranked matches featuring {champion_name}
- Analyze win rates by game length
- Examine performance vs. different team compositions
- Study laning phase statistics (CS, kills, deaths)

### 5. Champion Mastery Insights
Study dedicated {champion_name} players:
- Find players with high {champion_name} mastery points
- Analyze their match histories and performance patterns
- Identify skill progression indicators
- Compare different mastery approaches

### 6. Itemization Analysis
Examine current build meta:
- Core items vs. situational items
- Build order optimization
- Counter-building strategies
- Item synergies with champion kit

## Analysis Framework:

### Power Spikes:
- Level 1, 2, 3, 6, 9, 11, 16 power levels
- Item power spikes (first item, two-item, full build)
- Ability max order impact on power curve
- Late game scaling compared to other champions

### Matchup Analysis:
- Favorable matchups (champions {champion_name} counters)
- Difficult matchups (champions that counter {champion_name})
- Skill matchups requiring mechanical execution
- Team composition synergies

### Gameplay Patterns:
- Early game play style (aggressive, passive, farming)
- Mid game transition and objective control
- Late game team fighting role
- Macro gameplay contributions

### Statistical Benchmarks:
- Average KDA for skilled {champion_name} players
- CS benchmarks by game time
- Damage per minute expectations
- Vision score standards for the role

## Advanced Analysis Topics:

### Mechanical Complexity:
- Skill floor vs. skill ceiling assessment
- Combo execution requirements
- Animation canceling and optimization techniques
- Micro vs. macro skill importance

### Team Fighting:
- Primary role in team fights
- Positioning requirements and safety
- Engagement patterns and cooldown management
- Synergy with popular support/jungle champions

### Lane Phase:
- Trading patterns and power windows
- Farming efficiency and CS optimization
- Roaming potential and map pressure
- Teleport usage and side lane management

## Output Structure:

### 1. Champion Overview
- Role and position in current meta
- Difficulty rating and learning curve
- Key strengths and weaknesses

### 2. Performance Analytics
- Win rates across different skill levels
- Pick/ban frequency in ranked/professional play
- Statistical benchmarks for success

### 3. Optimal Builds & Runes
- Most successful item builds by situation
- Rune configurations and their use cases
- Skill order optimization

### 4. Matchup Guide
- Favorable and unfavorable matchups
- Laning strategies for different opponents
- Team composition considerations

### 5. Gameplay Guide
- Early/mid/late game priorities
- Team fighting positioning and combos
- Macro gameplay contributions

### 6. Learning Path
- Progression from beginner to advanced
- Key skills to develop
- Practice recommendations

Use multiple data sources and cross-reference findings to ensure accuracy. Present data-driven insights while acknowledging meta shifts and patch dependencies.
"""
        
        return prompt

    @mcp.prompt(name="team_composition_analysis", description="Analyze team composition effectiveness")
    async def team_comp_analysis_prompt(champions: str = "Azir,Graves,Thresh,Jinx,Malphite", region: str = "na1") -> str:
        """Generate analysis for a specific team composition.
        
        Args:
            champions: Comma-separated list of 5 champions
            region: Region for analysis
        """
        logger.info(f"Prompt called: team_comp_analysis_prompt(champions={champions})")
        
        champion_list = [c.strip() for c in champions.split(',')]
        
        prompt = f"""
# Team Composition Analysis

Analyzing team composition: **{' | '.join(champion_list)}** in region **{region.upper()}**

## Composition Breakdown:

### Champions to Analyze:
{chr(10).join([f"- {champion}" for champion in champion_list])}

## Analysis Framework:

### 1. Role Assignment
Identify the role each champion typically plays:
- Top lane champion and play style
- Jungle champion and ganking pattern
- Mid lane champion and roaming potential
- ADC champion and scaling pattern
- Support champion and utility level

### 2. Win Condition Analysis
Determine how this team wins games:
- **Early Game**: Identify early game strength
- **Mid Game**: Power spike timings and objective control
- **Late Game**: Scaling potential and team fighting

### 3. Team Fighting Dynamics
Analyze team fight execution:
- **Engage Tools**: Who initiates fights and how
- **Damage Sources**: Primary and secondary damage dealers
- **Protection**: How carries are kept safe
- **CC Chain**: Crowd control layering potential
- **AOE vs Single Target**: Damage distribution type

### 4. Synergy Assessment
Examine champion interactions:
- **Combo Potential**: Multi-champion combos available
- **Follow-up Chains**: How abilities chain together
- **Utility Stacking**: Overlapping buffs/debuffs
- **Coverage**: Damage types and crowd control variety

### 5. Weakness Identification
Find composition vulnerabilities:
- **Range Issues**: Poke vs. engage weaknesses
- **Mobility Gaps**: Kiting and chase potential
- **Damage Windows**: When the team is vulnerable
- **Resource Dependencies**: Mana/cooldown reliance

## Detailed Analysis Steps:

### Match Data Collection:
- Find recent matches featuring similar team compositions
- Analyze win rates when these champions are picked together
- Study game length correlations with success rate
- Examine performance against common enemy team archetypes

### Champion Interaction Mapping:
- Use champion static data to understand ability synergies
- Calculate total team damage potential at different stages
- Assess crowd control duration and layering
- Evaluate escape/disengage options

### Meta Positioning:
- Compare against current popular team compositions
- Identify counterpick vulnerabilities
- Assess adaptation potential in draft phase
- Evaluate flex pick options

### Statistical Validation:
- Find high-level matches with similar compositions
- Calculate average game statistics for this team type
- Benchmark against other composition archetypes
- Identify key performance indicators for success

## Composition Archetypes to Consider:

### Engage Compositions:
- Hard initiation with follow-up damage
- Dive potential and backline access
- Crowd control chains and lockdown

### Poke Compositions:
- Long-range damage and siege potential
- Disengage tools and kiting ability
- Objective control through poke pressure

### Split Push Compositions:
- 1-3-1 or 4-1 map control
- Side lane pressure with team fight ability
- Teleport coordination and map movement

### Scaling Compositions:
- Late game insurance and team fight power
- Stall tactics and defensive capabilities
- Item dependency and power curve timing

### Pick Compositions:
- Single target burst and elimination
- Vision control and pick setup
- Map control through threat presence

## Strategic Recommendations:

### Draft Phase:
- Pick order optimization
- Ban priorities against counters
- Flex pick utilization
- Counter-adaptation strategies

### Game Plan:
- Early game objectives and priorities
- Mid game transition timing
- Late game win condition execution
- Map control strategies

### Itemization:
- Core builds for team synergy
- Situational adaptations
- Power spike coordination
- Defensive itemization needs

## Expected Output:

### 1. Composition Summary
- Archetype classification
- Power rating (1-10) at different game stages
- Primary win condition

### 2. Synergy Analysis
- Key champion interactions
- Combo potential and execution
- Teamfight role distribution

### 3. Counter-Analysis
- Vulnerable composition types
- Key threats to watch for
- Adaptation strategies

### 4. Execution Guide
- Early game priorities
- Mid game transitions
- Late game team fighting
- Macro gameplay approach

Use match data and champion statistics to validate theoretical analysis. Consider patch-specific balance changes that might affect the composition's viability.
"""
        
        return prompt

    @mcp.prompt(name="player_improvement", description="Personalized improvement plan for a League player")
    async def player_improvement_prompt(game_name: str = "Player", tag_line: str = "NA1", target_rank: str = "Gold", current_role: str = "ADC") -> str:
        """Generate a personalized improvement plan for a League of Legends player.
        
        Args:
            game_name: Player's game name
            tag_line: Player's tag line
            target_rank: Desired rank to achieve
            current_role: Main role being played
        """
        logger.info(f"Prompt called: player_improvement_prompt(game_name={game_name}, target_rank={target_rank})")
        
        prompt = f"""
# Personalized Improvement Plan for {game_name}#{tag_line}

Creating a comprehensive improvement roadmap to reach **{target_rank}** as a **{current_role}** player.

## Initial Assessment Phase:

### 1. Current Performance Analysis
Gather baseline data:
- Use `get_account_by_riot_id` and `get_summoner_by_puuid` for player info
- Get current ranked status with `get_league_entries_by_summoner`
- Analyze recent match history (last 20-30 games) for patterns
- Calculate current performance metrics:
  - Average KDA
  - CS per minute
  - Vision score
  - Damage per minute
  - Win rate trends

### 2. Champion Pool Assessment
Evaluate champion expertise:
- Use `get_champion_masteries_by_puuid` for mastery data
- Analyze win rates on most played champions
- Identify comfort picks vs. meta picks
- Assess champion diversity and role flexibility

### 3. Match Pattern Analysis
Deep dive into gameplay patterns:
- Game length correlation with performance
- Performance in different phases (early/mid/late)
- Solo queue vs. premade performance
- Queue type preferences and success rates

## Skill Gap Analysis:

### Mechanical Skills ({current_role} Specific):
Based on {current_role} requirements:

#### If ADC:
- Last hitting accuracy and CS benchmarks
- Positioning in team fights
- Auto-attack spacing and kiting
- Ability weaving and animation canceling

#### If Support:
- Warding efficiency and vision control
- Roaming timing and map presence
- Peel mechanics and positioning
- Engage timing and follow-up

#### If Mid:
- Wave management and roaming
- Burst combos and ability accuracy
- Map awareness and TP usage
- Assassin vs. mage mechanics

#### If Jungle:
- Pathing efficiency and clear speed
- Gank timing and success rate
- Objective control and smite usage
- Counter-jungling and tracking

#### If Top:
- Trade pattern optimization
- Split push vs. team fight balance
- Teleport usage and timing
- Tank vs. carry role adaptation

### Macro Skills:
- Objective prioritization
- Map awareness and vision
- Wave management principles
- Team fighting positioning
- Late game decision making

## Improvement Roadmap:

### Phase 1: Foundation Building (2-4 weeks)
**Immediate Focus Areas:**
1. **Champion Pool Optimization**
   - Narrow to 2-3 champions maximum
   - Focus on meta-relevant picks
   - Master one comfort pick completely

2. **Fundamental Mechanics**
   - CS improvement (target: 7+ CS/min by 15 minutes)
   - Vision score improvement
   - Death reduction (identify avoidable deaths)

3. **Basic Macro Concepts**
   - Objective timing and priority
   - Back timing optimization
   - Map awareness drills

### Phase 2: Skill Development (4-6 weeks)
**Advanced Concepts:**
1. **Role-Specific Mastery**
   - Advanced mechanics for main champions
   - Role-specific game knowledge
   - Matchup understanding and adaptation

2. **Team Fighting**
   - Positioning optimization
   - Target selection and priority
   - Ability usage timing and efficiency

3. **Macro Strategy**
   - Wave management advanced concepts
   - Split push vs. group decision making
   - Late game shot-calling

### Phase 3: Consistency & Climbing (6-8 weeks)
**Performance Optimization:**
1. **Mental Game**
   - Tilt management and mental reset
   - Loss streak handling
   - Performance consistency

2. **Adaptation Skills**
   - Meta adaptation and champion updates
   - Team composition understanding
   - Counter-building and itemization

## Specific Improvement Metrics:

### {target_rank} Benchmarks:
Research typical {target_rank} player statistics:
- Average CS/min requirements
- Expected vision score ranges
- KDA expectations for {current_role}
- Win rate consistency targets

### Weekly Progress Tracking:
- Match review sessions (2-3 replays/week)
- Statistics comparison week-over-week
- Specific skill practice (practice tool usage)
- Ranked performance monitoring

## Practice Routine:

### Daily (30-45 minutes):
- 10 minutes practice tool (CS, combos)
- 2-3 ranked games maximum
- 1 replay review from previous session

### Weekly (deeper analysis):
- Compare current week vs. previous stats
- Identify recurring mistakes
- Adjust champion pool if needed
- Set next week's focus areas

## Data-Driven Tracking:

### Use API Tools for Progress Monitoring:
- Weekly rank progression tracking
- Match history analysis for trends
- Champion performance comparison
- Meta shift adaptation assessment

### Key Performance Indicators:
- Win rate in last 20 games
- Average game statistics improvement
- Consistency metrics (standard deviation)
- Specific skill benchmarks for {current_role}

## Common Pitfalls to Avoid:
- Playing too many different champions
- Ignoring macro for mechanical improvement
- Tilting and playing through loss streaks
- Not adapting to meta changes
- Focusing on teammates instead of self-improvement

## Success Milestones:
- Consistent positive win rate (55%+)
- Meeting role-specific statistical benchmarks
- Successful climb through divisions
- Maintained performance across multiple patches

Generate personalized recommendations based on actual player data and create specific, measurable goals for reaching {target_rank} as a {current_role} main.
"""
        
        return prompt 