#!/bin/bash

# Script Name: incremental_backup.sh
# Description: This Bash script automates the process of creating and managing incremental backups of a source directory.
# Author: Konstantinos Tsamis
# Date: 27/09/2023

# Usage:
#   - Ensure that you have properly set the source_dir, backup_dir, and num_backups_to_keep variables to match your specific setup.
#   - Run the script regularly to perform incremental backups.
#   - The script will create backup folders with a timestamp in the specified backup directory.
#   - It will automatically delete older backups if the number of backups exceeds the specified limit (num_backups_to_keep).
#   - When prompted, you can choose whether to delete an older backup or keep it.

# Configuration Variables:
#   - source_dir: The source directory to be backed up.
#   - backup_dir: The directory where backup folders will be stored.
#   - num_backups_to_keep: The maximum number of backups to retain.

# Example Usage:
#   1. Configure the source_dir, backup_dir, and num_backups_to_keep variables to match your setup.
#   2. Run the script periodically to create incremental backups of your source directory.
#   3. The script will automatically manage and delete older backups to maintain the specified limit.

# Note:
#   - This script uses the rsync command to perform incremental backups efficiently.
#   - It also checks if backups are older than the specified limit and offers the option to delete them.

# Disclaimer: Use this script at your own risk. Ensure that your backup strategy meets your data retention requirements.

# End of Description

# Define ANSI escape codes for colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

# Source and destination directories
source_dir=""
backup_dir=""
log_file=""

# Number of backups to keep (adjust as needed)
num_backups_to_keep=5

# Normalize paths to eliminate double slashes
source_dir=$(realpath "$source_dir")
backup_dir=$(realpath "$backup_dir")

# Function for initial backup
perform_initial_backup() {
    local current_date
    current_date=$(date "+%Y%m%d%H%M%S")

    # Create a new backup folder
    local backup_folder="$backup_dir/backup_$current_date"
    mkdir -p "$backup_folder"

    # Perform the initial backup using rsync and log the progress
    rsync -av "$source_dir" "$backup_folder" >> "$log_file" 2>&1
}

# Function for incremental backup
perform_incremental_backup() {
    local current_date
    current_date=$(date "+%Y%m%d%H%M%S")

    # Create a new backup folder
    local backup_folder="$backup_dir/backup_$current_date"
    mkdir -p "$backup_folder"

    # Perform an incremental backup using rsync and log the progress
    rsync -av --link-dest="$backup_dir/$(ls -t "$backup_dir" | tail -n 1)" "$source_dir" "$backup_folder" >> "$log_file" 2>&1
    echo -e "${GREEN}The backup is complete!"
    echo  # Add a blank line for spacing
}

# Function to confirm deletion
confirm_deletion() {
    local backup_to_delete="$1"

    # Check if the backup is older than the number of backups to keep
    backup_count=$(ls -dt "$backup_dir/backup_"* | wc -l)

    if [ "$backup_count" -gt "$num_backups_to_keep" ]; then
        echo -e "${YELLOW}Warning: This backup is too old because it exceeds the number of backups we keep. We will delete it.${NC}"
    fi

    # Display the backup name
    echo -e "${GREEN}Backup: $backup_to_delete${NC}"

    # Use the diff command to list files in the backup but not in the source
    diff_result=$(diff -rq "$backup_to_delete/original" "$source_dir" | grep "Only in $backup_to_delete/original" | cut -d' ' -f4-)

    if [ -n "$diff_result" ]; then
        echo -e "${RED}Files no longer in the source but present in the backup:${NC}"
        echo "$diff_result"
    else
        echo "No files removed from the source in this backup."
    fi

    read -n 1 -p "$(echo -e "${RED}Proceed with deleting this backup? (y/n): ${NC}")" confirm
    echo  # Add a newline for better formatting

    if [ "$confirm" = "y" ]; then
        rm -rf "$backup_to_delete"
        echo -e "${RED}Backup deleted: ${NC} $backup_to_delete"
        echo  # Add a blank line for spacing
    else
        echo "Backup deletion canceled."
        echo  # Add a blank line for spacing
    fi
}

# Function to delete the oldest backups until the desired number of backups is reached
delete_oldest_backups() {
    local backups=()
    mapfile -t backups < <(find "$backup_dir" -maxdepth 1 -type d -name "backup_*" | sort -r)

    for ((i = $num_backups_to_keep; i < ${#backups[@]}; i++)); do
        echo  # Add a blank line for spacing
        confirm_deletion "${backups[i]}"
    done
}

# Check if the destination directory doesn't exist and perform initial backup
if [ ! -d "$backup_dir" ]; then
    echo -e "${GREEN}Performing initial backup..."
    perform_initial_backup
else
    # Perform an incremental backup
    echo -e "${GREEN}Performing incremental backup..."
    perform_incremental_backup

    # Delete the oldest backup if the number of backups exceeds the limit
    delete_oldest_backups
fi

