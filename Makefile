# Fleet colour/type contract (fleet-ui/fleet.css), scoped to this repo so it
# can't go red because another app drifted. fleet-ui is a sibling clone and may
# be absent; say so and carry on.
FLEET_CHECK := $(CURDIR)/../fleet-ui/check.sh
check:
	@if [ -f "$(FLEET_CHECK)" ]; then \
	  bash "$(FLEET_CHECK)" "$(CURDIR)/dashboard"; \
	else \
	  echo "fleet check: skipped — no check.sh at $(FLEET_CHECK)"; \
	fi

.PHONY: check
