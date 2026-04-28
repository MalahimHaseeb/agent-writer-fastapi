"""Blog writing agent graph - orchestrates the workflow."""

from typing import Callable, Dict
from agent import AgentState, GraphOutput
from agent.nodes import router_node
from agent.nodes.search import search_node
from agent.nodes.writer import writer_node
from agent.nodes.critic import critic_node
from agent.nodes.formatter import formatter_node
from logger import setup_logger

logger = setup_logger(__name__)


class AgentGraph:
    """Blog writing agent workflow graph.
    
    Orchestrates the workflow:
    1. Router: Decides if search is needed
    2. Search: Performs web research (if needed)
    3. Writer: Generates initial draft
    4. Critic: Reviews and improves draft
    5. Formatter: Extracts metadata
    """

    def __init__(self):
        """Initialize the agent graph."""
        self.nodes: Dict[str, Callable] = {
            "router": router_node,
            "search": search_node,
            "writer": writer_node,
            "critic": critic_node,
            "formatter": formatter_node,
        }
        self.edges = [
            ("router", "search_decision"),  # Conditional edge
            ("search", "writer"),
            ("writer", "critic"),
            ("critic", "formatter"),
        ]

    async def _execute_router(self, state: AgentState) -> AgentState:
        """Execute router node."""
        logger.debug("[Graph] Executing router node")
        return await self.nodes["router"](state)

    async def _execute_search_decision(self, state: AgentState) -> AgentState:
        """Execute conditional edge - decide search or skip."""
        if state.needs_search:
            logger.debug("[Graph] Router decision: SEARCH")
            return await self.nodes["search"](state)
        else:
            logger.debug("[Graph] Router decision: SKIP")
            return state

    async def _execute_writer(self, state: AgentState) -> AgentState:
        """Execute writer node."""
        logger.debug("[Graph] Executing writer node")
        return await self.nodes["writer"](state)

    async def _execute_critic(self, state: AgentState) -> AgentState:
        """Execute critic node."""
        logger.debug("[Graph] Executing critic node")
        return await self.nodes["critic"](state)

    async def _execute_formatter(self, state: AgentState) -> AgentState:
        """Execute formatter node."""
        logger.debug("[Graph] Executing formatter node")
        return await self.nodes["formatter"](state)

    async def invoke(self, state: AgentState) -> AgentState:
        """Execute the complete workflow.
        
        Args:
            state: Initial agent state
            
        Returns:
            Final agent state with results
        """
        logger.info(f"[Graph] Starting workflow for topic: '{state.topic}'")

        try:
            # Sequential execution
            state = await self._execute_router(state)
            state = await self._execute_search_decision(state)
            state = await self._execute_writer(state)
            state = await self._execute_critic(state)
            state = await self._execute_formatter(state)

            logger.info("[Graph] Workflow completed successfully")
            return state

        except Exception as e:
            logger.error(f"[Graph] Workflow error: {str(e)}")
            return state.update(error=str(e))


# Singleton instance
_graph: AgentGraph = None


def get_graph() -> AgentGraph:
    """Get agent graph singleton."""
    global _graph
    if _graph is None:
        _graph = AgentGraph()
    return _graph


async def run_agent(topic: str, session_id: str) -> GraphOutput:
    """Run the blog writing agent.
    
    Args:
        topic: Blog topic to write about
        session_id: Session identifier
        
    Returns:
        Graph output with final blog and metadata
    """
    # Create initial state
    state = AgentState(
        topic=topic,
        session_id=session_id,
        search_results=[],
        needs_search=True,
        draft="",
        final_blog="",
        meta=None,
        error=None,
    )

    # Get and execute graph
    graph = get_graph()
    result_state = await graph.invoke(state)

    # Return results
    return GraphOutput(
        final_blog=result_state.final_blog or "",
        meta=result_state.meta,
        error=result_state.error,
    )
