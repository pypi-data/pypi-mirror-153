# Asynchronous message queues for Pip.Services in Python Changelog


## <a name="3.1.2"></a> 3.1.2 (2022-05-30)

### Bug Fixes
* Fixed thread safety for CachedMessageQueue, MemoryMessageQueue

## <a name="3.1.0"></a> 3.1.0 (2021-05-11)

### Bug Fixes
* fixed imports in tests

### Features
* Added connect and test package
* Update MemoryMessageQueue
* To build added IMessageQueueFactory, MessageQueueFactory
* To queues added CachedMessageQueue, CallbackMessageReceiver, LockedMessage
* Added type hints
* Update MessageEnvelope
* MessageQueue added abstract methods:
    - _check_open
    - is_open
    - close
    - clear
    - read_message_count
    - send methods
    - peek
    - peek_batch
    - receive
    - renew_lock
    - complete
    - abandon
    - move_to_dead_letter
    - listen
    - end_listen

## <a name="3.0.1-3.0.2"></a> 3.0.1-3.0.2 (2020-08-01)

### Bug Fixes
* fixed imports in tests

## <a name="3.0.0"></a> 3.0.0 (2018-10-22)

### New release
Initial public release

### Features
- **Build** - message queues factories
- **Queues** - asynchronous message queues
