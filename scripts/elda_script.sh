#!/bin/bash -x                                                                                                                                                                                                                                                                                                                                                                                                                                                    

echo "enter local or remote"

read response



case $response in

    local )

    echo "Entered LOCAL DVN"

    DVN_SERVER="localhost:8181" ;;

    remote )

    echo "Entered REMOTE DVN"

    # host="jpjones.lts.harvard.edu" ;;

    # DVN_SERVER="dvn-build.hmdc.harvard.edu" ;;

    DVN_SERVER="apitest.dataverse.org" ;;

    * )

    echo "you're supposed to enter REMOTE or LOCAL, stupid" ;;

esac



echo "you have chosen "$DVN_SERVER" as the dvn network."

echo -n "Enter USERNAME [ENTER]: "

read USERNAME

echo -n "Enter PASSWORD [ENTER]: "

read PASSWORD





echo "1. get service document"

curl --insecure -s https://$USERNAME:$PASSWORD@$DVN_SERVER/dvn/api/data-deposit/v1/swordv2/service-document | xmllint -format -



echo "2. create a dataset"

echo "enter DATAVERSE_ALIAS [ENTER]:"

read DATAVERSE_ALIAS

curl -s --insecure --data-binary "@data/atom-entry-study.xml" -H "Content-Type: application/atom+xml" -u $USERNAME:$PASSWORD https://$DVN_SERVER/dvn/api/data-deposit/v1/swordv2/collection/dataverse/$DATAVERSE_ALIAS | xmllint -format -



echo "3. Lists datasets"

echo "enter DATAVERSE_ALIAS [ENTER]:"

read DATAVERSE_ALIAS

curl --insecure -s -u $USERNAME:$PASSWORD https://$DVN_SERVER/dvn/api/data-deposit/v1/swordv2/collection/dataverse/$DATAVERSE_ALIAS | xmllint -format -



echo "4.Display a study statement (contains feed of file entries)"

echo "enter dataset GLOBAL_ID"

read GLOBAL_ID

curl --insecure -s https://$USERNAME:$PASSWORD@$DVN_SERVER/dvn/api/data-deposit/v1/swordv2/statement/study/$GLOBAL_ID


echo "5. Publish a dataset"

echo "enter dataset GLOBAL_ID"

read GLOBAL_ID

cat /dev/null | curl -s --insecure -X POST -H "In-Progress: false" --data-binary @- https://$USERNAME:$PASSWORD@$DVN_SERVER/dvn/api/data-deposit/v1/swordv2/edit/study/$GLOBAL_ID | xmllint --format -



echo "6. Deaccession a dataset (released studies only)"

echo "enter dataset GLOBAL_ID"

read GLOBAL_ID

curl -i --insecure -s -X DELETE https://$USERNAME:$PASSWORD@$DVN_SERVER/dvn/api/data-deposit/v1/swordv2/edit/study/$GLOBAL_ID


echo "7. Delete a dataset"

echo "enter dataset GLOBAL_ID"

read GLOBAL_ID

curl --insecure -i -X DELETE -u $USERNAME:$PASSWORD https://$DVN_SERVER/dvn/api/data-deposit/v1/swordv2/edit/study/$GLOBAL_ID


echo "8. Determine if a dataverse has been released (dataverseHasBeenReleased boolean)"

echo "enter DATAVERSE_ALIAS [ENTER]:"

read DATAVERSE_ALIAS

curl --insecure -s https://$USERNAME:$PASSWORD@$DVN_SERVER/dvn/api/data-deposit/v1/swordv2/collection/dataverse/$DATAVERSE_ALIAS | xmllint -format -



echo "9. publish a dataverse"

echo "enter DATAVERSE_ALIAS [ENTER]:"

read DATAVERSE_ALIAS

cat /dev/null | curl -s --insecure -X POST -H "In-Progress: false" --data-binary @- https://$USERNAME:$PASSWORD@$DVN_SERVER/dvn/api/data-deposit/v1/swordv2/edit/dataverse/$DATAVERSE_ALIAS | xmllint --format -