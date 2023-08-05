#!/bin/bash
echo ""
echo "*** Uploading dsframework documentation to google storage bucket ***"
echo ""
echo "Reading doxygen config..."
# Get documentation folder
doc_folder="not_found_yet"
html_folder_name="html"
google_gs_doc_folder="gs://dozi-stg-ds-apps-1-ds-apps-ds-portal/documentation/dsframework"
google_gs_backup_folder="gs://dozi-stg-ds-apps-1-ds-apps-ds-portal/documentation/backups"
google_storage_path='https://storage.cloud.google.com/dozi-stg-ds-apps-1-ds-apps-ds-portal/documentation/dsframework/'

IFS="="
while read -r name value
do
  trim_name=$(echo "$name" | tr -s " ")
  trim_name=${trim_name%% }
  trim_name=${trim_name## }

  if [ "$trim_name" == "OUTPUT_DIRECTORY" ];
  then
    doc_folder=${value//\"/}
    doc_folder=${doc_folder%% }
    doc_folder=${doc_folder## }
    #echo "Content of -$name- is -${value//\"/}-"
  fi
done < dsf_doxyfile

echo $doc_folder

if [ ! -d "$doc_folder/$html_folder_name" ]; then
  echo "DSF Documentation location not found, run the script from dsframework/documentation/ folder or "
  echo "create documentation using the following command:"
  echo ""
  echo "doxygen dsf_doxyfile"
  echo ""
  exit 1
fi

echo ""
echo "Moving current documentation to backup..."
backup_folder_name=$(date +"%y_%m_%d_%H_%M_%S")
backup_folder_name+="_dsframework"

# Rename
gsutil_move_command="gsutil -m mv ${google_gs_doc_folder} ${google_gs_backup_folder}/${backup_folder_name}"
eval $gsutil_move_command

# Insert <base> tag
echo ""
echo "Inserting <base> tag to documentation..."
python_modify_command="python scripts/doxygen_handler.py ${doc_folder}/${html_folder_name} ${google_storage_path}${html_folder_name}/"
echo $python_modify_command
eval $python_modify_command

# Copy
echo ""
echo "Uploading documentation..."
gsutil_copy_command="gsutil -m cp -r ${doc_folder}/${html_folder_name} ${google_gs_doc_folder}/${html_folder_name}"
echo $gsutil_copy_command
eval $gsutil_copy_command

echo ""
echo "Done!!!"

