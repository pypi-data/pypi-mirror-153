from puft.core.app.turbo_action_enum import TurboActionEnum
from warepy import Singleton
from puft.tools.log import log

from ..app.puft import Puft


class Emt(Singleton):
    """Emt is a special class performing various tasks related to turbo.js actions, such as updating.
    
    It acts with Views, which call methods from Emts.
    """
    def __init__(self, puft: Puft) -> None:
        self.puft = puft

    def push(
        self, action: TurboActionEnum, target: str, template_path: str, ctx_data: dict = {}  
    ) -> None:
        """Push turbo action to target with rendered from path template contextualized with given data.
        
        Args:
            action: Turbo-Flask action to perform.
            target: Id of HTML element to push action to.
            template_path: Path to template to render.
            ctx_data (optional): Context data to push to rendered template. Defaults to empty dict.
        """
        self.puft.push_turbo(
            action=action,
            target=target,
            template_path=template_path,
            ctx_data=ctx_data
        )
