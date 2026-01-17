from .confused_deputy import ConfusedDeputyAttack
from .synthetic_identity import SyntheticIdentityAbuse
from .plugin_impersonation import PluginImpersonation
from .toctou_privilege_escalation import TOCTOUPrivilegeEscalation
from .cross_agent_confusion import CrossAgentConfusion

__all__ = [
    ConfusedDeputyAttack,
    SyntheticIdentityAbuse,
    PluginImpersonation,
    TOCTOUPrivilegeEscalation,
    CrossAgentConfusion,
]
