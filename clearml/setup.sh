#!/bin/bash
echo "Running setup script."
source /root/venv/bin/activate
pip install clearml
# go to the repo directory
cd $CLEARML_GIT_ROOT

# now we need to tell clearml to use the python from our poetry env
# this is in the general case (we use the system python above, so we could
# have just hardcoded this as well)
export venv_python_path="/root/venv/bin/python"
echo "Detected poetry python: $venv_python_path"
cat > $CLEARML_CUSTOM_BUILD_OUTPUT << EOL
{
  "binary": "$venv_python_path",
  "entry_point": "$CLEARML_GIT_ROOT/$CLEARML_TASK_SCRIPT_ENTRY",
  "working_dir": "$CLEARML_GIT_ROOT/$CLEARML_TASK_WORKING_DIR"
}
EOL
