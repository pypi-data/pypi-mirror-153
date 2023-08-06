# SageMaker Studio Analytics Extension

This is a notebook extension provided by AWS SageMaker Studio Team to integrate with analytics resources. Currently, it supports connecting SageMaker Studio Notebook to Spark(EMR) cluster through SparkMagic library.

## Usage
Before you can use the magic command to connect Studio notebook to EMR, please ensure the SageMaker Studio has the connectivity to Spark cluster(livy service). You can refer to [this AWS blog](https://aws.amazon.com/blogs/machine-learning/amazon-sagemaker-studio-notebooks-backed-by-spark-in-amazon-emr/) for how to set up SageMaker Studio and EMR cluster. 
### Register the magic command:
```buildoutcfg
%load_ext sagemaker_studio_analytics_extension.magics
```
### Show help content:
```buildoutcfg
 %sm_analytics?
  
Docstring:
::

  %sm_analytics [--auth-type AUTH_TYPE] [--cluster-id CLUSTER_ID]
                    [--language LANGUAGE]
                    [--assumable-role-arn ASSUMABLE_ROLE_ARN]
                    [--emr-execution-role-arn EMR_EXECUTION_ROLE_ARN]
                    [command [command ...]]

positional arguments:
  command               Command to execute. The command consists of a service
                        name followed by a ' ' followed by an operation.
                        Supported services are ['emr'] and supported
                        operations are ['connect']. For example a valid
                        command is 'emr connect'.

optional arguments:
  --auth-type AUTH_TYPE
                        The authentication type to be used. Supported
                        authentication types are {'Kerberos', 'None',
                        'Basic_Access'}.
  --cluster-id CLUSTER_ID
                        The cluster id to connect to.
  --language LANGUAGE   Language to use. The supported languages for IPython
                        kernel(s) are {'python', 'scala'}. This is a required
                        argument for IPython kernels, but not for magic
                        kernels such as PySpark or SparkScala.
  --assumable-role-arn ASSUMABLE_ROLE_ARN
                        The IAM role to assume when connecting to a cluster in 
                        a different AWS account. This argument is not required 
                        when connecting to a cluster in the same AWS account.
  --emr-execution-role-arn EMR_EXECUTION_ROLE_ARN
                        The IAM role passed to EMR to set up EMR job security
                        context. This argument is optional and used when IAM
                        Passthrough feature is enabled for EMR.
```

### Examples
1. Connect Studio notebook using IPython Kernel to EMR cluster protected by Kerberos. 
```buildoutcfg
%sm_analytics emr connect --cluster-id j-1JIIZS02SEVCS --auth-type Kerberos --language python
```

2. Connect Studio notebook using IPython Kernel to HTTP Basic Auth protected EMR cluster and create the Scala based session.  
```buildoutcfg
%sm_analytics emr connect --cluster-id j-1KHIOQZAQUF5P --auth-type Basic_Access  --language scala
```

3. Connect Studio notebook using IPython Kernel to EMR cluster directly without Livy authentication. 
```buildoutcfg
%sm_analytics emr connect --cluster-id j-1KHIOQZAQUF5P --auth-type None  --language python
```

4. Connect Studio notebook using PySpark or Spark(scala) Kernel to HTTP Basic Auth protected EMR cluster. 
```buildoutcfg
%sm_analytics emr connect --cluster-id j-1KHIOQZAQUF5P --auth-type Basic_Access
```
## License

This library is licensed under the Apache 2.0 License. See the LICENSE file.

