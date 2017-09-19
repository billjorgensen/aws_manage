#!/bin/bash #-x
#
# Title: ec2_modify_sgs.sh
#
# Description: ec2_update_sgs.sh uses AWS CLI to either add or revoke ingress
# and egress entries. This is an interactive script.
#
# Usage: ec2_modify_sgs.sh
#
# Requirements
# - AWS CLI installed
# - appropriate AWS account IAM privileges to make changes to EC2 SGs
# - Python 2.7.12 or 3.5.2
#
# Change record
# 20170919-1123 - first pass that will update AWS SGs one at a time given the
# information prompted for
# 20170919-1351 - added ability to do the same rule in a different region with
# a different cidr
#
#############################################################
# variables
export PATH=${PATH}:/usr/local/bin:/usr/local/admin/bin:/usr/local/sbin:/usr/local/terraform:/usr/local/admin/sql/bin:/usr/local/admin/aws/billing

# function to add ingress rules
function add_ingress {
   # ask for port range, cidr and protocol
   echo -n "
   From_port: "
   read FromPort
   echo -n "
   To_port: "
   read ToPort
   echo -n "
   CIDR block: "
   read Cidr
   echo -n "
   Protocol (tcp): "
   read Prot
   echo -n "
   Does this need to be added in another region? (yes|no) "
   read Other

   # show existing...
   aws ec2 --region ${AwsReg} --output text describe-security-groups --group-ids ${SgId}
   if [ ${FromPort} = ${ToPort} ]
   then
      aws ec2 --region ${AwsReg} authorize-security-group-ingress --group-id ${SgId} --protocol ${Prot} --port ${FromPort} --cidr ${Cidr}
    else
      aws ec2 --region ${AwsReg} authorize-security-group-ingress --group-id ${SgId} --protocol ${Prot} --cidr ${Cidr} --port ${FromPort}-${ToPort}
    fi
   # show new...
   aws ec2 --region ${AwsReg} --output text describe-security-groups --group-ids ${SgId}

   # do work in the other region
   if [ "${Other}" = "yes" ]
   then
     echo -n "
 What region? "
     read OtherReg
     OtherId=`aws ec2 --region ${OtherReg} --output text describe-security-groups --filters "Name=group-name,Values=${SgName}" --query 'SecurityGroups[].[GroupId]'`
     echo -n "
 What CIDR? "
     read OtherCidr
     if [ ${FromPort} = ${ToPort} ]
     then
        aws ec2 --region ${OtherReg} authorize-security-group-ingress --group-id ${OtherId} --protocol ${Prot} --port ${FromPort} --cidr ${OtherCidr}
      else
        aws ec2 --region ${OtherReg} authorize-security-group-ingress --group-id ${OtherId} --protocol ${Prot} --cidr ${OtherCidr} --port ${FromPort}-${ToPort}
      fi
    fi
   # show new...
   aws ec2 --region ${OtherReg} --output text describe-security-groups --group-ids ${OtherId}
}

# function to add egress rules
function add_egress {
   # ask for port range, cidr and protocol
   echo -n "
   From_port: "
   read FromPort
   echo -n "
   To_port: "
   read ToPort
   echo -n "
   CIDR block: "
   read Cidr
   echo -n "
   Protocol (tcp): "
   read Prot
   echo -n "
   Does this need to be added in another region? (yes|no) "
   read Other

   # show existing...
   aws ec2 --region ${AwsReg} --output text describe-security-groups --group-ids ${SgId}
   if [ ${FromPort} = ${ToPort} ]
   then
      aws ec2 --region ${AwsReg} authorize-security-group-egress --group-id ${SgId} --protocol ${Prot} --port ${FromPort} --cidr ${Cidr}
    else
      aws ec2 --region ${AwsReg} authorize-security-group-egress --group-id ${SgId} --protocol ${Prot} --cidr ${Cidr} --port ${FromPort}-${ToPort}
    fi
   # show new...
   aws ec2 --region ${AwsReg} --output text describe-security-groups --group-ids ${SgId}

   # do work in the other region...
   if [ "${Other}" = "yes" ]
   then
     echo -n "
 What region? "
     read OtherReg
     OtherId=`aws ec2 --region ${OtherReg} --output text describe-security-groups --filters "Name=group-name,Values=${SgName}" --query 'SecurityGroups[].[GroupId]'`
     echo -n "
 What CIDR? "
     read OtherCidr
     if [ ${FromPort} = ${ToPort} ]
     then
        aws ec2 --region ${OtherReg} authorize-security-group-egress --group-id ${OtherId} --protocol ${Prot} --port ${FromPort} --cidr ${OtherCidr}
      else
        aws ec2 --region ${OtherReg} authorize-security-group-egress --group-id ${OtherId} --protocol ${Prot} --cidr ${OtherCidr} --port ${FromPort}-${ToPort}
      fi
    fi
   # show new...
   aws ec2 --region ${OtherReg} --output text describe-security-groups --group-ids ${OtherId}
}

# function to revoke ingress rules
function revoke_ingress {
   # ask for port range, cidr and protocol
   echo -n "
   From_port: "
   read FromPort
   echo -n "
   To_port: "
   read ToPort
   echo -n "
   CIDR block: "
   read Cidr
   echo -n "
   Protocol (tcp): "
   read Prot
   echo -n "
   Does this need to be added in another region? (yes|no) "
   read Other

   # show existing...
   aws ec2 --region ${AwsReg} --output text describe-security-groups --group-ids ${SgId}
   if [ ${FromPort} = ${ToPort} ]
   then
      aws ec2 --region ${AwsReg} revoke-security-group-ingress --group-id ${SgId} --protocol ${Prot} --port ${FromPort} --cidr ${Cidr}
    else
      aws ec2 --region ${AwsReg} revoke-security-group-ingress --group-id ${SgId} --protocol ${Prot} --cidr ${Cidr} --port ${FromPort}-${ToPort}
    fi
   # show new...
   aws ec2 --region ${AwsReg} --output text describe-security-groups --group-ids ${SgId}

   # do work in the other region...
   if [ "${Other}" = "yes" ]
   then
     echo -n "
 What region? "
     read OtherReg
     OtherId=`aws ec2 --region ${OtherReg} --output text describe-security-groups --filters "Name=group-name,Values=${SgName}" --query 'SecurityGroups[].[GroupId]'`
     echo -n "
 What CIDR? "
     read OtherCidr
     if [ ${FromPort} = ${ToPort} ]
     then
        aws ec2 --region ${OtherReg} revoke-security-group-ingress --group-id ${OtherId} --protocol ${Prot} --port ${FromPort} --cidr ${OtherCidr}
      else
        aws ec2 --region ${OtherReg} revoke-security-group-ingress --group-id ${OtherId} --protocol ${Prot} --cidr ${OtherCidr} --port ${FromPort}-${ToPort}
      fi
    fi
   # show new...
   aws ec2 --region ${OtherReg} --output text describe-security-groups --group-ids ${OtherId}
}

# function to revoke egress rules
function revoke_egress {
   # ask for port range, cidr and protocol
   echo -n "
   From_port: "
   read FromPort
   echo -n "
   To_port: "
   read ToPort
   echo -n "
   CIDR block: "
   read Cidr
   echo -n "
   Protocol (tcp): "
   read Prot
   echo -n "
   Does this need to be added in another region? (yes|no) "
   read Other

   # show existing...
   aws ec2 --region ${AwsReg} --output text describe-security-groups --group-ids ${SgId}
   if [ ${FromPort} = ${ToPort} ]
   then
      aws ec2 --region ${AwsReg} revoke-security-group-egress --group-id ${SgId} --protocol ${Prot} --port ${FromPort} --cidr ${Cidr}
    else
      aws ec2 --region ${AwsReg} revoke-security-group-egress --group-id ${SgId} --protocol ${Prot} --cidr ${Cidr} --port ${FromPort}-${ToPort}
    fi
   # show new...
   aws ec2 --region ${AwsReg} --output text describe-security-groups --group-ids ${SgId}

   # do work in the other region...
   if [ "${Other}" = "yes" ]
   then
     echo -n "
 What region? "
     read OtherReg
     OtherId=`aws ec2 --region ${OtherReg} --output text describe-security-groups --filters "Name=group-name,Values=${SgName}" --query 'SecurityGroups[].[GroupId]'`
     echo -n "
 What CIDR? "
     read OtherCidr
     if [ ${FromPort} = ${ToPort} ]
     then
        aws ec2 --region ${OtherReg} revoke-security-group-egress --group-id ${OtherId} --protocol ${Prot} --port ${FromPort} --cidr ${OtherCidr}
      else
        aws ec2 --region ${OtherReg} revoke-security-group-egress --group-id ${OtherId} --protocol ${Prot} --cidr ${OtherCidr} --port ${FromPort}-${ToPort}
      fi
    fi
   # show new...
   aws ec2 --region ${OtherReg} --output text describe-security-groups --group-ids ${OtherId}
}

# function to get information
function task_todo {
   # need to prompt for the info...
   echo -n "
   What needs to be done?
      1. Add ingress
      2. Revoke ingress
      3. Add egress
      4. Revoke egress

   Response: "
   read ToDo
   #echo ${ToDo}
   # get the region
   echo -n "
   Please provide the AWS region (us-west-1, us-west-2, us-east-1): "
   read AwsReg
   if [ "${AwsReg}" = "us-west-1" -o "${AwsReg}" = "us-west-2" -o "${AwsReg}" = "us-east-1" ]
   then
     echo "   Region ok..."
   else
     echo "
   NOTICE: Invalid AWS Region! Valid regions are: us-west-1, us-west-2, and us-east-1
   Please check your response and begin again...
   "
    exit 2
   fi
   # get the sg name...
   echo -n "
   Please provide the AWS SG Name: "
   read SgName
   # go fetch the aws sg id using the info...
   SgId=`aws ec2 --region ${AwsReg} --output text describe-security-groups --filters "Name=group-name,Values=${SgName}" --query 'SecurityGroups[].[GroupId]'`
   if [ "X${SgId}" = "X" ]
   then
     echo "
   NOTICE: SG not found! Please check the name a begin again...
   "
     exit 1
   fi
}

# main portion and usage...
case ${1} in
   -h|--help|-?|--?)
      echo "
   Usage: `basename $0`
       "
       exit 1
      ;;
   "")
      task_todo
      #echo "${ToDo}"
      if [ ${ToDo} = 1 ]
      then
        add_ingress
      elif [ ${ToDo} = 2 ]
      then
        revoke_ingress
      elif [ ${ToDo} = 3 ]
      then
        add_egress
      elif [ ${ToDo} = 4 ]
      then
        revoke_egress
      fi
      ;;
esac
exit 0
