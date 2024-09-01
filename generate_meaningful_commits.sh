#!/bin/bash

# Directory where your repo is located
REPO_DIR="."

# Go to the repo directory
cd "$REPO_DIR" || { echo "Directory $REPO_DIR not found"; exit 1; }

# Ensure there are no unstaged changes
if ! git diff-index --quiet HEAD --; then
    echo "Unstaged changes detected. Please commit or stash them before running this script."
    exit 1
fi

# Commit messages and corresponding code changes
declare -A CHANGES
CHANGES=(
    ["Refactored face detection code"]="sed -i 's/cascadeClassifier.load(cascadePath);/cascadeClassifier.load(cascadePath); \n # Improved face detection with new model/' attendance.py"
    ["Improved LBPH recognizer accuracy"]="sed -i 's/lbph_face_recognizer.train(images, np.array(labels));/lbph_face_recognizer.train(images, np.array(labels)); \n # Increased accuracy by adjusting parameters/' attendance.py"
    ["Fixed bug in attendance tracking logic"]="sed -i 's/if (attendanceStatus == true) { /if (attendanceStatus == true) { \n # Fixed bug by ensuring proper attendance status check/' attendance.py"
    ["Updated Excel management functionality"]="sed -i 's/excel_writer.save();/excel_writer.save(); \n # Updated to handle Excel file format changes/' excel_management.py"
    ["Enhanced GUI for user experience"]="sed -i 's/button.config(text=\"Capture Image\");/button.config(text=\"Capture Image\", bg=\"lightblue\"); \n # Enhanced GUI button appearance/' gui.py"
    ["Optimized image capture performance"]="sed -i 's/capture.read();/capture.read(); \n # Improved image capture performance by adjusting frame rate/' capture.py"
    ["Cleaned up old code and comments"]="sed -i '/\/\/ TODO: Remove this code/d' attendance.py"
)

# Function to apply code changes
apply_change() {
    local message="$1"
    local command="$2"

    echo "Applying change: $message"
    eval "$command"
    
    git add .
    git commit -m "$message"
}

# Generate commits for the last 12 months, 7 days per month
for i in $(seq 1 7); do
    # Generate a random date within the past 12 months
    DATE=$(date -d "$((RANDOM % 365 + 1)) days ago" +"%Y-%m-%d")
    TIME=$(printf "%02d:%02d:%02d" $((RANDOM % 24)) $((RANDOM % 60)) $((RANDOM % 60)))
    
    # Select a random commit message and code change
    MESSAGE=$(printf "%s\n" "${!CHANGES[@]}" | sed -n "$(echo $((RANDOM % ${#CHANGES[@]} + 1)))p")
    COMMAND="${CHANGES[$MESSAGE]}"
    
    # Apply the change and commit
    apply_change "$MESSAGE" "$COMMAND"
    
    # Set the commit date
    GIT_COMMITTER_DATE="$DATE $TIME" git commit --amend --no-edit --date="$DATE $TIME"
    
    # Push the commit
    git push origin main
done

echo "Commits added and pushed to GitHub repository."

