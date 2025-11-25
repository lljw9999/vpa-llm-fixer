import re
import sys
import io
import contextlib
import multiprocessing
import traceback
from typing import List, Dict, Any, Optional

class CodeExecutor:
    """
    Executes Python code snippets extracted from text.
    WARNING: This uses exec() and is NOT sandboxed. Use only with trusted models/prompts.
    """

    def __init__(self, timeout: int = 5):
        """
        Initialize the code executor.
        
        Args:
            timeout: Maximum execution time in seconds (default: 5)
        """
        self.timeout = timeout

    def extract_code_blocks(self, text: str) -> List[str]:
        """
        Extract Python code blocks from markdown text.
        
        Args:
            text: Markdown text containing code blocks
            
        Returns:
            List of code strings
        """
        # Match ```python ... ``` or just ``` ... ```
        # The regex handles optional 'python' tag and captures content
        pattern = r"```(?:python)?\s*(.*?)\s*```"
        matches = re.findall(pattern, text, re.DOTALL)
        return [match.strip() for match in matches if match.strip()]

    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        Execute a code snippet with timeout.
        
        Args:
            code: Python code to execute
            
        Returns:
            Dictionary with 'success', 'output', 'error'
        """
        # Create a queue to get results from the process
        queue = multiprocessing.Queue()
        
        # Create a process to run the code
        process = multiprocessing.Process(
            target=self._run_code_in_process,
            args=(code, queue)
        )
        
        process.start()
        process.join(self.timeout)
        
        if process.is_alive():
            process.terminate()
            process.join()
            return {
                "success": False,
                "output": "",
                "error": f"Execution timed out after {self.timeout} seconds"
            }
            
        if not queue.empty():
            return queue.get()
        else:
            return {
                "success": False,
                "output": "",
                "error": "Process failed to return result"
            }

    @staticmethod
    def _run_code_in_process(code: str, queue: multiprocessing.Queue):
        """
        Worker function to run code in a separate process.
        """
        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        result = {
            "success": False,
            "output": "",
            "error": ""
        }
        
        try:
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                # Create a restricted globals dictionary if needed, but for MVP we use default
                # We execute in a clean namespace
                exec_globals = {}
                exec(code, exec_globals)
                
            result["success"] = True
            result["output"] = stdout_capture.getvalue()
            result["error"] = stderr_capture.getvalue()
            
        except Exception:
            result["success"] = False
            result["output"] = stdout_capture.getvalue()
            # Capture full traceback
            result["error"] = f"{stderr_capture.getvalue()}\n{traceback.format_exc()}".strip()
            
        queue.put(result)
