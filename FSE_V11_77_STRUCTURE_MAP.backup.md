# FSE V11.77 STRUCTURE MAP

## Project Phase
Production Architecture Organization Phase

## Purpose
This document records the clean architecture organization
of FSE before dependency integration.

Rules:
- No production code modification in this phase.
- No deletion without dependency verification.
- No fake logic.
- No simulation logic inside production modules.
- Legacy modules remain isolated until reviewed.
- One folder completion before moving to the next.

---

# Brain Architecture Map

## 1. Core Brain / Intelligence Core

Responsibility:
- Main intelligence processing
- Adaptive behavior
- Autonomous reasoning foundation

Files:

adaptive_brain.py
adaptive_brain_v10_27.py
autonomous_brain.py
autonomous_master_brain_v10_17.py
autonomous_general_intelligence_core_v10_40.py
autonomous_intelligence_core_v10_20.py
autonomous_intelligence_core_v10_67.py
memory_integrated_brain_v10_19.py
self_adaptive_brain_v10_15.py

Status:
Mapped - Pending Integration Order

---
# 2. Decision Layer

Responsibility:
- Market information evaluation
- Decision generation
- Confidence analysis
- Predictive decision support

Files:

decision_engine.py
autonomous_decision_engine_v10_66.py
predictive_decision_fusion_v10_34.py
inference_engine.py
confidence.py

Status:
Mapped - Pending Integration Order


---


# 3. Learning & Memory Layer

Responsibility:
- Continuous learning
- Experience storage
- Memory management
- Feedback processing

Files:

adaptive_learning_engine_v10_64.py
adaptive_learning_v10_5.py
learning_memory_v10_64.py
experience_learning_engine_v10_36.py
experience_learning_engine_v2.py
long_term_memory_v10_18.py
persistent_memory.py
performance_memory.py
reward_engine.py
reward_engine_v10_63.py

Status:
Mapped - Pending Integration Order

---
# 4. Market Intelligence Layer

Responsibility:
- Market understanding
- Market context preparation
- Market regime analysis
- Price and trend intelligence

Files:

market_analysis.py
market_feed.py
market_intelligence_bridge.py
market_regime.py
market_scanner.py
price_monitor.py
trend_engine.py
volatility_engine.py

Status:
Mapped - Pending Integration Order


---


# 5. Risk Intelligence Layer

Responsibility:
- Risk control
- Risk evaluation
- Capital protection
- Risk state management

Files:

risk_adapter.py
risk_engine.py
autonomous_risk_engine.py
autonomous_risk_intelligence_v10_43.py
risk_governor.py
risk_memory.py

Status:
Mapped - Pending Integration Order

---
# 6. Portfolio Intelligence Layer

Responsibility:
- Capital allocation
- Portfolio management
- Position control
- Portfolio optimization

Files:

portfolio_engine.py
portfolio_manager.py
portfolio_allocator_v9_4.py
portfolio_intelligence.py
portfolio_rebalancer.py
portfolio_rebalancer_v9_6.py
portfolio_memory.py
portfolio_memory_loop_v9_7.py
position_engine.py
position_manager.py
position_sizing_engine.py
autonomous_adaptive_portfolio_intelligence_v10_49.py
autonomous_portfolio_intelligence_v10_12.py
autonomous_portfolio_optimization_engine_v10_48.py
autonomous_portfolio_state_manager_v10_46.py
capital_allocator.py
dynamic_allocator.py

Status:
Mapped - Pending Integration Order


---


# 7. Execution Intelligence Layer

Responsibility:
- Order execution lifecycle
- Execution control
- Trade persistence
- Execution feedback

Files:

execution_engine.py
execution_manager.py
execution_persistence.py
execution_risk_guard.py
execution_feedback_bridge.py
trade_feedback_bridge.py
trade_feedback_engine_v10_61.py
closed_trade_handler.py

Status:
Mapped - Pending Integration Order

---
# 8. Signal & Strategy Intelligence Layer

Responsibility:
- Signal generation
- Feature analysis
- Strategy input preparation
- Market opportunity detection

Files:

signal_engine.py
signal_pipeline.py
signals.py
feature_engine.py
alpha_universe.py
predictor.py
reversal_engine.py
trend_engine.py
grid_engine.py

Status:
Mapped - Pending Integration Order


---


# 9. Control / Orchestration Layer

Responsibility:
- System coordination
- Module communication
- High-level execution flow
- Component orchestration

Files:

orchestrator.py
orchestrator_v2.py
orchestrator_v3.py
orchestrator_v3_1.py

autonomous_brain_orchestrator_v10_41.py

autonomous_controller_v2.py
autonomous_controller_v7.py
autonomous_controller_v8_2.py
autonomous_controller_v8_3.py
autonomous_controller_v8_5.py
autonomous_controller_v8_8.py
autonomous_controller_v8_9.py
autonomous_controller_v9_3.py
autonomous_controller_v9_5.py

Status:
Mapped - Pending Integration Order

---
# 10. State Management Layer

Responsibility:
- Runtime state handling
- System memory state
- Persistence coordination
- Recovery state foundation

Files:

autonomous_state_v10_1.py
autonomous_state_v10_10.py
autonomous_state_manager_v10_22.py
state_storage.py
memory_manager.py
intelligence_state_store_v10_68.py
autonomous_memory.py

Status:
Mapped - Pending Integration Order


---


# 11. Self Improvement & Evolution Layer

Responsibility:
- Self optimization
- Performance improvement
- Adaptive evolution
- Continuous enhancement

Files:

autonomous_evolution_engine_v10_30.py
self_evolution_learning_loop_v10_38.py
self_optimizer.py
self_optimizer_v10_6.py
self_optimizer_v10_26.py
autonomous_self_improving_brain_v10_28.py
optimization_core.py
performance_intelligence_v10_25.py

Status:
Mapped - Pending Integration Order

---
# 12. Runtime Governance Layer (V10 Foundation)

Responsibility:
- Runtime supervision
- Health monitoring
- Lifecycle control
- Governance foundation

Files:

intelligence_runtime_health_v10_71.py
intelligence_runtime_health_manager_v10_85.py
intelligence_runtime_monitoring_service_v10_86.py
intelligence_runtime_monitoring_supervisor_v10_87.py

intelligence_runtime_state_coordinator_v10_81.py
intelligence_runtime_state_supervisor_v10_82.py

intelligence_runtime_persistence_supervisor_v10_79.py
intelligence_runtime_recovery_supervisor_v10_80.py

intelligence_runtime_lifecycle_coordinator_v10_83.py
intelligence_runtime_lifecycle_supervisor_v10_84.py

intelligence_runtime_manager_v10_94.py
intelligence_runtime_orchestrator_v10_97.py
intelligence_runtime_coordinator_v10_96.py
intelligence_runtime_controller_v10_98.py
intelligence_runtime_supervisor_v10_95.py
intelligence_runtime_supervisor_controller_v10_99.py

Status:
Mapped - Pending Integration Order


---
# 13. V11 Governance Recovery Chain

Responsibility:
- Runtime governance control
- Recovery coordination
- Failure handling
- Autonomous governance decision flow

## V11 Recovery Foundation

Files:

v11_59_controller_coordinator_manager.py
v11_60_controller_coordinator_manager_supervisor.py
v11_61_runtime_controller.py
v11_62_runtime_controller_hardening.py
v11_63_runtime_recovery_controller.py
v11_64_recovery_supervisor.py
v11_65_recovery_coordinator.py
v11_66_recovery_coordinator_manager.py
v11_67_recovery_governance.py
v11_68_recovery_governance_supervisor.py
v11_69_recovery_governance_coordinator.py
v11_70_recovery_governance_manager.py

Status:
Mapped - Pending Integration Order


---


# 14. V11.71 - V11.77 Governance Runtime Core

Responsibility:
- Governance runtime execution
- Decision governance
- Runtime supervision
- Recovery integration

Files:

v11_71_governance_runtime_controller.py
v11_71_runtime_governance_engine.py
v11_72_autonomous_runtime_control.py
v11_72_governance_recovery_supervisor.py
v11_73_autonomous_runtime_supervisor.py
v11_73_governance_recovery_coordinator.py
v11_74_autonomous_runtime_governor.py
v11_74_governance_recovery_manager.py
v11_75_autonomous_runtime_decision_engine.py
v11_75_governance_runtime_governance.py
v11_76_autonomous_runtime_decision_supervisor.py
v11_76_governance_runtime_controller.py
v11_77_autonomous_runtime_decision_governance.py
v11_77_governance_runtime_supervisor.py

Status:
Mapped - Pending Integration Order

---
# 15. V11.78 - V11.99 Autonomous Runtime Decision Governance Extensions

Responsibility:
- Autonomous decision governance
- Execution governance chain
- Runtime coordination extensions
- Supervisor and controller hierarchy

Files:

v11_78_autonomous_runtime_decision_governance_supervisor.py
v11_79_autonomous_runtime_decision_governance_coordinator.py
v11_80_autonomous_runtime_decision_governance_manager.py
v11_81_autonomous_runtime_decision_governance_controller.py
v11_82_autonomous_runtime_decision_governance_runtime.py
v11_83_autonomous_runtime_decision_governance_supervisor_runtime.py
v11_84_autonomous_runtime_decision_governance_coordinator_runtime.py
v11_85_autonomous_runtime_decision_governance_manager_runtime.py
v11_86_autonomous_runtime_decision_governance_controller_runtime.py
v11_87_autonomous_runtime_decision_governance_execution_runtime.py
v11_88_autonomous_runtime_decision_governance_execution_supervisor.py
v11_89_autonomous_runtime_decision_governance_execution_coordinator.py
v11_90_autonomous_runtime_decision_governance_execution_manager.py
v11_91_autonomous_runtime_decision_governance_execution_controller.py
v11_92_autonomous_runtime_decision_governance_execution_orchestrator.py
v11_93_autonomous_runtime_decision_governance_execution_orchestrator_supervisor.py
v11_94_autonomous_runtime_decision_governance_execution_orchestrator_supervisor_runtime.py
v11_95_autonomous_runtime_decision_governance_execution_orchestrator_supervisor_runtime_manager.py
v11_96_autonomous_runtime_decision_governance_execution_orchestrator_supervisor_runtime_controller.py
v11_97_autonomous_runtime_decision_governance_execution_orchestrator_supervisor_runtime_controller_manager.py
v11_98_autonomous_runtime_decision_governance_execution_orchestrator_supervisor_runtime_controller_manager_runtime.py
v11_99_autonomous_runtime_decision_governance_execution_orchestrator_supervisor_runtime_controller_manager_runtime_supervisor.py

Status:
Mapped - Pending Integration Order

---
# 16. Learning, Memory & Feedback Intelligence Layer

Responsibility:
- Continuous learning
- Experience processing
- Feedback analysis
- Long term intelligence improvement

Files:

adaptive_learning_v10_5.py
adaptive_learning_engine_v10_64.py
autonomous_learning_engine_v10_24.py
autonomous_learning_cycle_v9_9.py
autonomous_learning_coordinator_v10_65.py
autonomous_learning_integration_v10_37.py

experience_learning_engine_v2.py
experience_learning_engine_v10_36.py

learning_memory_v10_64.py
long_term_memory_v10_18.py
persistent_memory.py
performance_memory.py
performance_memory_v10_62.py

decision_memory_replay_v10_35.py
reward_engine.py
reward_engine_v10_63.py

feedback_engine.py
feedback_loop.py
execution_feedback_bridge.py
trade_feedback_bridge.py
trade_feedback_engine_v10_61.py

Status:
Mapped - Pending Integration Order


---


# 17. Trading Intelligence Supporting Layer

Responsibility:
- Market analysis
- Position intelligence
- Portfolio intelligence
- Risk awareness

Files:

market_analysis.py
market_regime.py
market_scanner.py
market_intelligence_bridge.py
market_portfolio_integration.py

portfolio_engine.py
portfolio_manager.py
portfolio_allocator_v9_4.py
portfolio_intelligence.py
portfolio_feedback.py
portfolio_memory.py
portfolio_memory_loop_v9_7.py
portfolio_rebalancer.py
portfolio_rebalancer_v9_6.py

position_engine.py
position_manager.py
position_sizing_engine.py

risk_adapter.py
risk_engine.py
risk_governor.py
risk_memory.py

capital_allocator.py
dynamic_allocator.py
profit_manager.py
smart_exit.py
exit_strategy.py
closed_trade_handler.py

Status:
Mapped - Pending Integration Order

---
# 18. Brain Supporting Components Layer

Responsibility:
- Supporting intelligence utilities
- Scanning components
- Operational helpers
- Internal processing modules

Files:

auto_scanner.py
market_feed.py
model_loader.py
optimization_core.py
full_system.py
live_loop.py
live_learning_loop.py

hedge_engine.py
reversal_engine.py
trend_engine.py
volatility_engine.py

grid_engine.py
inference_engine.py
feature_engine.py

dynamic_allocator.py
confidence.py
predictor.py

performance_intelligence_v10_25.py
autonomous_performance_v10_4.py

Status:
Mapped - Pending Integration Order


---


# 19. Brain Architecture Completion Record

Folder:
brain/

Total Python Files Reviewed:
348 files

Architecture Groups Created:
19 layers

Current Status:

[✓] Core Intelligence mapped
[✓] Decision layer mapped
[✓] Learning & Memory mapped
[✓] Market Intelligence mapped
[✓] Risk Intelligence mapped
[✓] Portfolio Intelligence mapped
[✓] Execution Intelligence mapped
[✓] Signal & Strategy mapped
[✓] Control & Orchestration mapped
[✓] Runtime Governance mapped
[✓] V11 Governance Chain mapped
[✓] Supporting components mapped

Next Phase:

1. Complete remaining project folders.
2. Create dependency order.
3. Connect production architecture.
4. Run complete validation tests.

No production code changes during structure phase.

---
# 20. Adapters Layer

Folder:
adapters/

Responsibility:
- External system adaptation
- Exchange data conversion
- Interface standardization
- Communication bridge between external services and FSE core

Architecture Role:

External Exchange
        |
        v
Adapters Layer
        |
        v
Market / Execution / Strategy Core


## Market Data Adapters

Files:

market_data_adapter.py

Responsibility:
- Defines market data adapter contract
- Standard interface for market providers

Status:
Mapped - Pending Integration Order


binance_market_data_adapter.py

Responsibility:
- Binance market data conversion
- Exchange response to internal SymbolState mapping

Status:
Mapped - Pending Integration Order


binance_market_adapter.py

Responsibility:
- Binance market integration adapter

Status:
Mapped - Pending Integration Order


binance_adapter.py

Responsibility:
- Binance communication adapter foundation

Status:
Mapped - Pending Integration Order


---
# 21. Adapters Dependency Position

Layer Position:

External Services
        |
        v
Clients Layer
        |
        v
Adapters Layer
        |
        v
Domain Services
        |
        v
Brain / Strategy / Execution


## Adapter Dependency Rules

Rules:

- Adapters do not contain trading decisions.
- Adapters do not contain risk decisions.
- Adapters do not contain strategy logic.
- Adapters only translate external data/interfaces.
- Production adapters must connect to real providers.


## Current Adapter Components

### Binance Integration

Component:
Binance Adapter Family

Files:

binance_adapter.py
binance_market_adapter.py
binance_market_data_adapter.py

Purpose:

- Exchange communication bridge
- Market data transformation
- Standardized internal access


### Abstract Contract

File:

market_data_adapter.py

Purpose:

- Defines adapter interface
- Prevents direct dependency on exchange implementation


Status:

Adapters Folder:
Structure Mapped

Next:
Dependency Integration Order

---
# 22. Adapters Folder Completion Record

Folder:

adapters/


Reviewed Components:

[✓] Abstract Market Data Contract
[✓] Binance Market Adapter
[✓] Binance Market Data Adapter
[✓] Binance Exchange Adapter


Architecture Role:

Adapters are responsible for:

- External communication translation
- Exchange interface abstraction
- Data normalization
- Provider isolation


Integration Direction:

clients/
    |
    v
adapters/
    |
    v
market/
    |
    v
brain/


# 3. Clients Architecture Map

Folder:

clients/

Files:

__init__.py
binance_client.py
binance_market_data_client.py
binance_symbol_client.py


Architecture Role:

Clients are responsible for:

- External service communication
- Exchange API access layer
- Receiving raw external data
- Providing data access interface


Dependency Direction:

External Exchange
        |
        v
clients/
        |
        v
adapters/
        |
        v
market/


Current Status:

Clients Structure:
COMPLETED

---
# 3. Clients Architecture Map

Folder:

clients/

Files:

__init__.py
binance_client.py
binance_market_data_client.py
binance_symbol_client.py


Architecture Role:

Clients layer responsibilities:

- External service communication
- Exchange API access
- Raw external data retrieval
- Provider communication boundary


Dependency Direction:

External Exchange
        |
        v
clients/
        |
        v
adapters/
        |
        v
market/


Current Status:

Clients Structure:
COMPLETED

---
# 4. Config Architecture Map

Folder:

config/

Files:

constants.py
env_config.py
settings.py


Architecture Role:

Config layer responsibilities:

- Application configuration
- Environment settings
- Global constants management
- Runtime configuration boundary


Dependency Direction:

Environment
     |
     v
config/
     |
     v
clients/
     |
     v
adapters/
     |
     v
market/


Current Status:

Config Structure:
COMPLETED

---
# 5. Data Architecture Map

Folder:

data/

Files:

cache.py
normalization.py
storage.py
storage_handler.py


Legacy / Archived Reference Files:

data_collector_v11.77_before_archive.py
dataset_builder_v11.77_before_archive.py
dataset_builder_v11.77_before_fake_cleanup.py
loader_v11.77_before_archive.py


Architecture Role:

Data layer responsibilities:

- Data storage management
- Data normalization
- Local data handling
- Cache management


Dependency Direction:

External Data
      |
      v
data/
      |
      v
market/
      |
      v
brain/


Current Status:

Data Structure:
MAPPED

Legacy References:
ISOLATED

---
# 6. Docs Structure Map

Folder:

docs/

Python Files:

None


Architecture Role:

Documentation layer:

- Architecture records
- Project documentation
- Design references


Current Status:

Docs Structure:
NO PYTHON MODULES

---
# 7. Execution Architecture Map

Folder:

execution/

Files:

binance_executor.py
connection_tester.py
execution_engine.py
execution_listener.py
sl_tp_handler.py


Backup Reference Files:

connection_tester.backup.py
execution_engine.backup.py


Architecture Role:

Execution layer responsibilities:

- Exchange order execution boundary
- Execution flow management
- Execution event handling
- Stop loss and take profit handling


Dependency Direction:

strategy/
      |
      v
execution/
      |
      v
exchange


Current Status:

Execution Structure:
MAPPED

Backup Files:
ISOLATED

---
# 8. Market Architecture Map

Folder:

market/


Architecture Role:

Production market data subsystem.

Responsibilities:

- Exchange market data intake
- Market data processing pipeline
- Symbol discovery and activation
- Market runtime coordination
- Market state management
- Runtime monitoring and persistence


Core Components:

market_data_application.py
market_data_container.py
market_data_pipeline.py
market_data_service.py
market_data_runtime.py
market_data_scheduler.py
market_data_orchestrator.py
market_data_coordinator.py


Feed Components:

binance_client.py
binance_market_adapter.py
real_market_feed_adapter.py
market_feed_service.py
market_feed_scheduler.py


Symbol Components:

symbol_discovery_service.py
symbol_registry.py
symbol_activation_policy.py
market_symbol_activator.py
symbol_feed_manager.py


Runtime Components:

runtime_event_repository.py
runtime_health_repository.py
runtime_metrics_repository.py
runtime_state_repository.py
runtime_supervisor_metrics.py


Persistence Components:

sqlite_runtime_event_repository.py
sqlite_runtime_health_repository.py
sqlite_runtime_metrics_repository.py
sqlite_runtime_state_repository.py
sqlite_runtime_supervisor_metrics_repository.py


Architecture Direction:

Exchange
    |
    v
market/
    |
    v
brain/


Current Status:

Market Structure:
COMPLETED

---
# 9. Models Architecture Map

Folder:

models/


Files:

__init__.py
symbol_state.py


Architecture Role:

Models layer responsibilities:

- Domain data structures
- Shared data representation
- Market state modeling


Dependency Direction:

clients/
    |
    v
adapters/
    |
    v
models/
    |
    v
market/


Current Status:

Models Structure:
COMPLETED

---
# 10. Parsers Architecture Map

Folder:

parsers/


Files:

__init__.py
binance_exchange_parser.py
binance_market_data_parser.py


Architecture Role:

Parsers layer responsibilities:

- External data format conversion
- Exchange response parsing
- Data normalization boundary
- Conversion into internal representations


Dependency Direction:

clients/
    |
    v
parsers/
    |
    v
models/
    |
    v
market/


Current Status:

Parsers Structure:
COMPLETED

---
# 11. Portfolio Architecture Map

Folder:

portfolio/


Files:

allocation_engine.py
balance_tracker.py
manager.py
performance_report.py
pnl_calculator.py


Architecture Role:

Portfolio layer responsibilities:

- Capital allocation management
- Portfolio state tracking
- Balance management
- Profit and loss calculation
- Performance reporting


Dependency Direction:

strategy/
    |
    v
portfolio/
    |
    v
risk/
    |
    v
execution/


Current Status:

Portfolio Structure:
COMPLETED

---
# 12. Registry Architecture Map

Folder:

registry/


Files:

__init__.py
symbol_registry.py


Architecture Role:

Registry layer responsibilities:

- Symbol registration management
- Active symbol tracking
- Shared registry state access


Dependency Direction:

market/
    |
    v
registry/
    |
    v
strategy/


Current Status:

Registry Structure:
COMPLETED

---
/# 13. Repositories Architecture Map

Folder:

repositories/


Files:

__init__.py
in_memory_market_repository.py
market_repository.py
sqlite_market_repository.py


Architecture Role:

Repositories layer responsibilities:

- Data persistence abstraction
- Storage interface management
- Market state storage access
- Database implementation boundary


Dependency Direction:

market/
    |
    v
repositories/
    |
    v
storage


Current Status:

Repositories Structure:
COMPLETED

---
# 14. Risk Architecture Map

Folder:

risk/


Files:

hedge_controller.py
manager.py
max_drawdown_control.py
position_sizer.py
risk_manager.py


Architecture Role:

Risk layer responsibilities:

- Risk management control
- Position sizing
- Drawdown protection
- Hedging control
- Risk policy enforcement


Dependency Direction:

strategy/
    |
    v
risk/
    |
    v
portfolio/
    |
    v
execution/


Current Status:

Risk Structure:
COMPLETED

---
# 15. Services Architecture Map

Folder:

services/


Files:

__init__.py
market_data_service.py


Architecture Role:

Services layer responsibilities:

- Application service coordination
- Market data service access
- Business workflow boundary


Dependency Direction:

market/
    |
    v
services/
    |
    v
application runtime


Current Status:

Services Structure:
COMPLETED

---
/# 16. Strategy Architecture Map

Folder:

strategy/


Files:

__init__.py
alpha_strategy.py
grid_strategy.py
market_structure.py
mean_reversion.py
momentum_strategy.py
smc_strategy.py
strategy_router.py


Archived / Previous Version References:

grid_strategy_v11.77_before_refactor.py
mean_reversion_v11.77_before_refactor.py
strategy_router_v11.77_before_feed_fix.py


Architecture Role:

Strategy layer responsibilities:

- Trading decision logic
- Strategy execution routing
- Market structure interpretation
- Signal generation boundary


Dependency Direction:

market/
    |
    v
strategy/
    |
    v
risk/
    |
    v
execution/


Current Status:

Strategy Structure:
COMPLETED

---
# 17. Transport Architecture Map

Folder:

transport/


Files:

__init__.py
http_client.py


Architecture Role:

Transport layer responsibilities:

- External communication transport
- HTTP communication boundary
- Network request handling


Dependency Direction:

external services
      |
      v
transport/
      |
      v
clients/
      |
      v
adapters/


Current Status:

Transport Structure:
COMPLETED

---
# 18. Monitoring Architecture Map

Folder:

monitoring/


Files:

alert_engine.py
error_tracker.py
logger.py
performance_monitor.py
system_health.py


Architecture Role:

Monitoring layer responsibilities:

- System health observation
- Runtime performance tracking
- Error monitoring
- Alert management
- Operational logging


Dependency Direction:

runtime/
    |
    v
monitoring/
    |
    v
operators / control systems


Current Status:

Monitoring Structure:
COMPLETED

---
# 19. Utils Architecture Map

Folder:

utils/


Files:

decorators.py
helpers.py
math_utils.py
message_bus.py
time_utils.py
validators.py


Architecture Role:

Utils layer responsibilities:

- Shared helper functions
- Common validation utilities
- Internal communication helpers
- Time and calculation utilities


Dependency Direction:

all production modules
        |
        v
utils/


Current Status:

Utils Structure:
COMPLETED

---

# 20. Cloud Architecture Map

Folder:

cloud/


Files:

deployment_config.py
docker_setup.py
env_manager.py
oracle_adapter.py
scaling_manager.py


Architecture Role:

Cloud layer responsibilities:

- Deployment configuration
- Environment management
- Container setup
- Infrastructure scaling support
- External cloud provider integration boundary


Dependency Direction:

production runtime
        |
        v
cloud/


Current Status:

Cloud Structure:
COMPLETED

---
# 21. Telegram Architecture Map

Folder:

telegram/


Files:

alert_system.py
auth_guard.py
bot_handler.py
command_router.py
message_formatter.py


Architecture Role:

Telegram layer responsibilities:

- External notification interface
- Bot command handling
- Message formatting
- Access control boundary
- Alert communication


Dependency Direction:

monitoring/
    |
    v
telegram/
    |
    v
external users


Current Status:

Telegram Structure:
COMPLETED

---
# 22. P2P Architecture Map

Folder:

P2P/


Files:

__init__.py
p2p_api.py


Architecture Role:

P2P layer responsibilities:

- Peer communication interface
- Distributed communication boundary
- External node interaction support


Dependency Direction:

external peers
        |
        v
P2P/
        |
        v
application services


Current Status:

P2P Structure:
COMPLETED

---
# 23. Dashboard Architecture Map

Folder:

dashboard/


Files:

api_server.py
app.py
metrics_view.py
ui_state_manager.py
websocket_feed.py


Architecture Role:

Dashboard layer responsibilities:

- System visualization interface
- Runtime metrics display
- API presentation layer
- WebSocket data communication
- User interface state management


Dependency Direction:

monitoring/
    |
    v
dashboard/
    |
    v
operators / users


Current Status:

Dashboard Structure:
COMPLETED

---
# 24. Testing Infrastructure Map

Folder:

testing/


Files:

test_brain.py
test_execution.py
test_integration.py
test_risk.py
test_strategy.py


Architecture Role:

Testing layer responsibilities:

- Production validation support
- Integration test coverage
- Module behavior verification
- Regression protection


Rules:

- Testing code remains isolated.
- No test logic inside production modules.
- Production runtime does not depend on testing folder.


Dependency Direction:

production modules
        |
        v
testing/


Current Status:

Testing Structure:
COMPLETED

---
# 25. Tests Infrastructure Map

Folder:

tests/


Files:

test_binance_exchange_parser.py
test_binance_market_adapter_v10_58.py
test_symbol_registry_v10_58.py


Architecture Role:

Tests layer responsibilities:

- Component validation
- Parser testing
- Adapter testing
- Registry behavior verification


Rules:

- Tests remain isolated from production runtime.
- No production dependency on tests.
- No fake logic promoted into production.


Dependency Direction:

production modules
        |
        v
tests/


Current Status:

Tests Structure:
COMPLETED

---
# Data Architecture Map

Folder:

data/


Production Files:

cache.py
normalization.py
storage.py
storage_handler.py


Archived / Excluded Files:

data_collector_v11.77_before_archive.py
dataset_builder_v11.77_before_archive.py
dataset_builder_v11.77_before_fake_cleanup.py
loader_v11.77_before_archive.py


Architecture Role:

Data layer responsibilities:

- Data storage management
- Data normalization
- Cache handling
- Internal data persistence


Production Rules:

- No fake dataset generation.
- No simulation data in production.
- Legacy collectors remain isolated.


Dependency Direction:

market/
    |
    v
data/
    |
    v
repositories/


Current Status:

Data Structure:
COMPLETED

---
# Config Architecture Map

Folder:

config/


Files:

constants.py
env_config.py
settings.py


Architecture Role:

Config layer responsibilities:

- Runtime configuration management
- Environment variable handling
- Global application settings
- Shared constants


Production Rules:

- No secrets hardcoded.
- Environment-specific values remain externalized.
- Configuration does not contain business logic.


Dependency Direction:

environment
    |
    v
config/
    |
    v
production services


Current Status:

Config Structure:
COMPLETED

---
# Services Architecture Map

Folder:

services/


Files:

__init__.py
market_data_service.py


Architecture Role:

Services layer responsibilities:

- Application service boundary
- Market data service coordination
- Business workflow orchestration


Production Rules:

- No exchange-specific implementation inside service layer.
- No strategy decisions.
- No fake data generation.


Dependency Direction:

clients/
    |
    v
adapters/
    |
    v
market/
    |
    v
services/


Current Status:

Services Structure:
COMPLETED

---
# Clients Architecture Map

Folder:

clients/


Files:

__init__.py
binance_client.py
binance_market_data_client.py
binance_symbol_client.py


Architecture Role:

Clients layer responsibilities:

- External API communication
- Exchange client abstraction
- Provider request handling
- Raw external response retrieval


Production Rules:

- No strategy logic.
- No risk decisions.
- No execution decisions.
- No fake market data.


Dependency Direction:

external exchange
        |
        v
clients/
        |
        v
adapters/
        |
        v
market/


Current Status:

Clients Structure:
COMPLETED

---# Utils Architecture Map

Folder:

utils/


Files:

decorators.py
helpers.py
math_utils.py
message_bus.py
time_utils.py
validators.py


Architecture Role:

Utils layer responsibilities:

- Shared helper functions
- Common validation utilities
- Internal communication helpers
- Time management utilities
- Mathematical utilities


Production Rules:

- No business strategy logic.
- No risk decisions.
- No execution decisions.
- Shared utilities only.


Dependency Direction:

production modules
        |
        v
utils/


Current Status:

Utils Structure:
COMPLETED

---
