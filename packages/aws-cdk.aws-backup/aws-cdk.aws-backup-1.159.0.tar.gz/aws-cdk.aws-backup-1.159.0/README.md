# AWS Backup Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

AWS Backup is a fully managed backup service that makes it easy to centralize and automate the
backup of data across AWS services in the cloud and on premises. Using AWS Backup, you can
configure backup policies and monitor backup activity for your AWS resources in one place.

## Backup plan and selection

In AWS Backup, a *backup plan* is a policy expression that defines when and how you want to back up
your AWS resources, such as Amazon DynamoDB tables or Amazon Elastic File System (Amazon EFS) file
systems. You can assign resources to backup plans, and AWS Backup automatically backs up and retains
backups for those resources according to the backup plan. You can create multiple backup plans if you
have workloads with different backup requirements.

This module provides ready-made backup plans (similar to the console experience):

```python
# Daily, weekly and monthly with 5 year retention
plan = backup.BackupPlan.daily_weekly_monthly5_year_retention(self, "Plan")
```

Assigning resources to a plan can be done with `addSelection()`:

```python
# plan: backup.BackupPlan

my_table = dynamodb.Table.from_table_name(self, "Table", "myTableName")
my_cool_construct = Construct(self, "MyCoolConstruct")

plan.add_selection("Selection",
    resources=[
        backup.BackupResource.from_dynamo_db_table(my_table),  # A DynamoDB table
        backup.BackupResource.from_tag("stage", "prod"),  # All resources that are tagged stage=prod in the region/account
        backup.BackupResource.from_construct(my_cool_construct)
    ]
)
```

If not specified, a new IAM role with a managed policy for backup will be
created for the selection. The `BackupSelection` implements `IGrantable`.

To add rules to a plan, use `addRule()`:

```python
# plan: backup.BackupPlan

plan.add_rule(backup.BackupPlanRule(
    completion_window=Duration.hours(2),
    start_window=Duration.hours(1),
    schedule_expression=events.Schedule.cron( # Only cron expressions are supported
        day="15",
        hour="3",
        minute="30"),
    move_to_cold_storage_after=Duration.days(30)
))
```

Continuous backup and point-in-time restores (PITR) can be configured.
Property `deleteAfter` defines the retention period for the backup. It is mandatory if PITR is enabled.
If no value is specified, the retention period is set to 35 days which is the maximum retention period supported by PITR.
Property `moveToColdStorageAfter` must not be specified because PITR does not support this option.
This example defines an AWS Backup rule with PITR and a retention period set to 14 days:

```python
# plan: backup.BackupPlan

plan.add_rule(backup.BackupPlanRule(
    enable_continuous_backup=True,
    delete_after=Duration.days(14)
))
```

Ready-made rules are also available:

```python
# plan: backup.BackupPlan

plan.add_rule(backup.BackupPlanRule.daily())
plan.add_rule(backup.BackupPlanRule.weekly())
```

By default a new [vault](#Backup-vault) is created when creating a plan.
It is also possible to specify a vault either at the plan level or at the
rule level.

```python
my_vault = backup.BackupVault.from_backup_vault_name(self, "Vault1", "myVault")
other_vault = backup.BackupVault.from_backup_vault_name(self, "Vault2", "otherVault")

plan = backup.BackupPlan.daily35_day_retention(self, "Plan", my_vault) # Use `myVault` for all plan rules
plan.add_rule(backup.BackupPlanRule.monthly1_year(other_vault))
```

You can [backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/windows-backups.html)
VSS-enabled Windows applications running on Amazon EC2 instances by setting the `windowsVss`
parameter to `true`. If the application has VSS writer registered with Windows VSS,
then AWS Backup creates a snapshot that will be consistent for that application.

```python
plan = backup.BackupPlan(self, "Plan",
    windows_vss=True
)
```

## Backup vault

In AWS Backup, a *backup vault* is a container that you organize your backups in. You can use backup
vaults to set the AWS Key Management Service (AWS KMS) encryption key that is used to encrypt backups
in the backup vault and to control access to the backups in the backup vault. If you require different
encryption keys or access policies for different groups of backups, you can optionally create multiple
backup vaults.

```python
my_key = kms.Key.from_key_arn(self, "MyKey", "aaa")
my_topic = sns.Topic.from_topic_arn(self, "MyTopic", "bbb")

vault = backup.BackupVault(self, "Vault",
    encryption_key=my_key,  # Custom encryption key
    notification_topic=my_topic
)
```

A vault has a default `RemovalPolicy` set to `RETAIN`. Note that removing a vault
that contains recovery points will fail.

You can assign policies to backup vaults and the resources they contain. Assigning policies allows
you to do things like grant access to users to create backup plans and on-demand backups, but limit
their ability to delete recovery points after they're created.

Use the `accessPolicy` property to create a backup vault policy:

```python
vault = backup.BackupVault(self, "Vault",
    access_policy=iam.PolicyDocument(
        statements=[
            iam.PolicyStatement(
                effect=iam.Effect.DENY,
                principals=[iam.AnyPrincipal()],
                actions=["backup:DeleteRecoveryPoint"],
                resources=["*"],
                conditions={
                    "StringNotLike": {
                        "aws:userId": ["user1", "user2"
                        ]
                    }
                }
            )
        ]
    )
)
```

Alternativately statements can be added to the vault policy using `addToAccessPolicy()`.

Use the `blockRecoveryPointDeletion` property or the `blockRecoveryPointDeletion()` method to add
a statement to the vault access policy that prevents recovery point deletions in your vault:

```python
# backup_vault: backup.BackupVault
backup.BackupVault(self, "Vault",
    block_recovery_point_deletion=True
)
backup_vault.block_recovery_point_deletion()
```

By default access is not restricted.

## Importing existing backup vault

To import an existing backup vault into your CDK application, use the `BackupVault.fromBackupVaultArn` or `BackupVault.fromBackupVaultName`
static method. Here is an example of giving an IAM Role permission to start a backup job:

```python
imported_vault = backup.BackupVault.from_backup_vault_name(self, "Vault", "myVaultName")

role = iam.Role(self, "Access Role", assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))

imported_vault.grant(role, "backup:StartBackupJob")
```
