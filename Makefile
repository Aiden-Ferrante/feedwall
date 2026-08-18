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

# The 06:45 briefing's systemd units live in this repo rather than only in
# ~/.config/systemd/user, so the schedule and the script it runs have one
# history. SYMLINK, not copy: a copy is a second source of truth, where editing
# the repo and forgetting to reinstall leaves the file that actually runs
# disagreeing with the file under review. systemd reads through the link, so
# git pull + daemon-reload is the whole update path. Cost: moving or deleting
# this checkout breaks the units, which is the correct failure.
#
# The .service is `static` on purpose — no [Install] — because the timer is its
# only legitimate trigger; only the timer gets enabled.
UNITS := feedwall-briefing.service feedwall-briefing.timer
UNIT_DIR := $(HOME)/.config/systemd/user
install-unit:
	@mkdir -p "$(UNIT_DIR)"
	@for u in $(UNITS); do \
	  if [ -e "$(UNIT_DIR)/$$u" ] && [ ! -L "$(UNIT_DIR)/$$u" ]; then \
	    cp "$(UNIT_DIR)/$$u" "$(UNIT_DIR)/$$u.pre-repo.bak"; \
	    echo "kept the previous non-symlink unit at $(UNIT_DIR)/$$u.pre-repo.bak"; \
	  fi; \
	  ln -sfn "$(CURDIR)/deploy/$$u" "$(UNIT_DIR)/$$u"; \
	  echo "linked $(UNIT_DIR)/$$u -> $(CURDIR)/deploy/$$u"; \
	done
	systemctl --user daemon-reload
	systemctl --user enable --now feedwall-briefing.timer

.PHONY: check install-unit
