from .overprivileged_tool import OverprivilegedToolAbuse
from .overscoped_tool import OverscopedToolAbuse
from .unvalidated_input_forwarding import UnvalidatedInputForwarding
from .unsafe_browsing import UnsafeBrowsing
from .loop_amplification import LoopAmplification
from .external_data_poisoning import ExternalDataPoisoning
from .edr_bypass_chaining import EDRBypassChaining
from .tool_name_impersonation import ToolNameImpersonation
from .approved_tool_misuse import ApprovedToolMisuse

__all__ = [
    OverprivilegedToolAbuse,
    OverscopedToolAbuse,
    UnvalidatedInputForwarding,
    UnsafeBrowsing,
    LoopAmplification,
    ExternalDataPoisoning,
    EDRBypassChaining,
    ToolNameImpersonation,
    ApprovedToolMisuse,
]
