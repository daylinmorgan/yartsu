PHONIFY=true

-include .task.mk
$(if $(filter help,$(MAKECMDGOALS)),$(if $(wildcard .task.mk),,.task.mk: ; curl -fsSL https://raw.githubusercontent.com/daylinmorgan/task.mk/main/task.mk -o .task.mk))
