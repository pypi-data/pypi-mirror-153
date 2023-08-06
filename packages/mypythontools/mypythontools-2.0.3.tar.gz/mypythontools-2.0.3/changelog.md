# List of what have been done in new versions

## 0.1.x - 11/2021

- [x] Restructured to submodules
- [x] Tests now supports multiple python versions 
- [x] Config changed, so property is called with no function parameters. With parenthesis, it would fail. Reason is that annotations are now used for type and option checking, so less code and also for better IDE help and better intellisense. It is not possible to use custom getters and setters anymore.