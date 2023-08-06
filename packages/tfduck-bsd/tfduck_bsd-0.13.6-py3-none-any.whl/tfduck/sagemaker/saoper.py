"""
s3的公共操作
版本号见setup.py
"""
# coding=utf-8


class SAOper(object):
    """
    @des: S3的公共操作, 上传文件
    """

    def __init__(self, ctx={}):
        """
        @des: 初始化
        """
        self.ctx = ctx

    def submit_proccess_task(self,
                             sagemaker_session,
                             base_job_name,
                             image_uri,
                             role,
                             #
                             code,
                             arguments,
                             #
                             instance_count=1,
                             command=['/opt/program/submit'],
                             instance_type='ml.c5.xlarge',
                             max_runtime_in_seconds=86400,
                             env={'mode': 'python'},
                             #
                             logs=False,
                             wait=True,
                             retry_count=3  # 出错后重试次数
                             ):
        '''
        @des: 提交处理任务--例如特征值处理任务，特征值工程到sagemaker
        参考代码:
        ####
        def call_tzz_etl(self):
            ctx = self.ctx
            gconf = GAConfig.getInstance()
            from sagemaker import get_execution_role
            import sagemaker
            #
            s3_session = boto3.Session(
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name='us-east-2'
            )
            #
            sagemaker_session = sagemaker.Session(boto_session=s3_session)
            iam = s3_session.client('iam')
            role = iam.get_role(
                RoleName='AmazonSageMaker-ExecutionRole-20200817T105993')['Role']['Arn']
            #
            from sagemaker.sklearn.processing import SKLearnProcessor, ScriptProcessor
            from sagemaker.processing import ProcessingInput, ProcessingOutput
            """
            获取我自己创建的容器镜像资源
            """
            account_id = s3_session.client(
                'sts').get_caller_identity().get('Account')
            BMOBJ.clog(ctx, 111, self.part_date, account_id)
            # region = boto3.session.Session().region_name
            region = s3_session.region_name
            ecr_repository = 'sagemaker-spark-yx'
            tag = ':latest'
            uri_suffix = 'amazonaws.com'
            if region in ['cn-north-1', 'cn-northwest-1']:
                uri_suffix = 'amazonaws.com.cn'
            spark_repository_uri = '{}.dkr.ecr.{}.{}/{}'.format(
                account_id, region, uri_suffix, ecr_repository + tag)
            BMOBJ.clog(ctx, spark_repository_uri)
            """
            开始跑测试脚本
            """
            spark_processor = ScriptProcessor(
                sagemaker_session=sagemaker_session,
                base_job_name='bf-raw-to-tzz',  # 不能用下划线
                image_uri=spark_repository_uri,
                command=['/opt/program/submit'],
                role=role,
                # 容器数量，这里有点疑问，如果是多个，怎么并发处理； 解答：是将数据做了shard放到了不同机器上
                # 不要在作业里面做模型训练和推理， 还是要起另外的训练任务和批量转换任务来做
                instance_count=1,  # 最多 nxlarge == n*4
                instance_type='ml.c5.xlarge',  # c类型的比较省钱,
                max_runtime_in_seconds=86400,
                env={'mode': 'python'})
            # bucket = sagemaker_session.default_bucket()
            code_path = BMOBJ.get_file_path(
                'bf_hv_user_predit/bf_hv_user_predit_tf_2/src/preprocess/preprocess_tzz.py')
            BMOBJ.clog(ctx, 111, self.bucket, code_path)
            input_prefix = gconf.get_s3_key(
                ["hv_user_predit_raw", self.part_date, "*"])
            output_prefix = gconf.get_s3_key(
                ["hv_user_predit_tzz", self.part_date])
            spark_processor.run(code=code_path,  # 在本地路径下面
                                arguments=['s3_input_bucket', self.bucket,
                                        's3_input_key_prefix', input_prefix,
                                        's3_output_bucket', self.bucket,
                                        's3_output_key_prefix', output_prefix],
                                logs=False, wait=True)
            # 清空原始数据表
            if 0: # 不用spark
                spark = gconf.get_spark()
                input_path = gconf.get_s3a_path(["hv_user_predit_raw", self.part_date])
                df_empty = spark.createDataFrame([(0,)], ["empty"])
                df_empty.write.csv(input_path, mode='overwrite', header=False)
            else:
                s3o = S3Oper(ctx)
                remote_path = gconf.get_s3_key(["hv_user_predit_raw", self.part_date])
                BMOBJ.clog(ctx, f"remote path {remote_path}")
                s3o.delete_folder(remote_path)
            #
            BMOBJ.clog(ctx, "end")
        ####
        '''
        from sagemaker.sklearn.processing import SKLearnProcessor, ScriptProcessor
        from sagemaker.processing import ProcessingInput, ProcessingOutput
        for i in range(retry_count):
            try:

                spark_processor = ScriptProcessor(
                    sagemaker_session=sagemaker_session,
                    base_job_name=base_job_name,  # 不能用下划线
                    image_uri=image_uri,
                    command=command,
                    role=role,
                    # 容器数量，这里有点疑问，如果是多个，怎么并发处理； 解答：是将数据做了shard放到了不同机器上
                    # 不要在作业里面做模型训练和推理， 还是要起另外的训练任务和批量转换任务来做
                    instance_count=instance_count,  # 最多 nxlarge == n*4
                    instance_type=instance_type,  # c类型的比较省钱,
                    max_runtime_in_seconds=max_runtime_in_seconds,
                    env=env)
                spark_processor.run(code=code,  # 在本地路径下面
                                    arguments=arguments,
                                    logs=logs, wait=wait)
                break
            except Exception as e:
                if str(e).find("Rate exceeded") != -1:
                    continue
                else:
                    raise e
        return True

    def submit_batch_tran_task(
        self,
        model_name,
        sagemaker_session,
        output_path,
        data,
        instance_count=1,
        instance_type='ml.m4.xlarge',
        accept="text/csv",
        assemble_with="Line",
        data_type='S3Prefix',
        content_type='text/csv',
        split_type='Line',
        input_filter="$[3:]",
        join_source="Input",
        output_filter="$",
        retry_count=3
    ):
        '''
        @des: 提交批量转换任务
        参考代码
        ######
        def tran(self):
        """
        @des: 批量转换--测试结果集
        """
        ctx = self.ctx
        BMOBJ.clog(ctx, f"start tran {self.part_date}")
        gconf = GAConfig.getInstance()
        s3_session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name='us-east-2'
        )
        sagemaker_session = sagemaker.Session(boto_session=s3_session)
        # 预测的结果文件

        output_path = gconf.get_s3_path(
            ["hv_user_predit_tran", self.part_date, "tran"])
        output_path_s3a = gconf.get_s3a_path(
            ["hv_user_predit_tran", self.part_date, "tran"])
        output_path_key = gconf.get_s3_key(
            ["hv_user_predit_tran", self.part_date, "tran"])
        if 1:
            # 清空
            s3oper_obj = S3Oper(ctx)
            s3oper_obj.delete_folder(output_path_key)
            # 加强健壮性---特别注意train_data的路径前缀，不要和统计目录有混淆
            # 前缀一样会被当成一批，比如testsample111同级目录下有testsample111_xx都会被读到
            transformer = sagemaker.estimator.Transformer(model_name='bf-hv-user-train-model',
                                                          instance_count=1,
                                                          instance_type='ml.m4.xlarge',
                                                          sagemaker_session=sagemaker_session,
                                                          output_path=output_path,
                                                          accept="text/csv",   # 配合下面的join_source= "Input"
                                                          assemble_with="Line",  # 配合下面的join_source= "Input"
                                                          )
            tran_samples = gconf.get_s3_path(
                ["hv_user_predit_sample", self.part_date, 'predit'])
            tran_samples_3a = gconf.get_s3a_path(
                ["hv_user_predit_sample", self.part_date, 'predit'])
            BMOBJ.clog(ctx, tran_samples)
            #
            transformer.transform(data=tran_samples, data_type='S3Prefix',
                                  content_type='text/csv', split_type='Line',
                                  # 这里特别注意，$[a:b]是要取到b的和python的分片不太一样,所以这里不取最后一个元素，用-2
                                  # 不取第一列的用户id
                                  input_filter="$[3:]",
                                  join_source="Input",
                                  output_filter="$"
                                  )
            transformer.wait()
            BMOBJ.clog(ctx, "batch tran end")
        ######
        '''
        import sagemaker
        for i in range(retry_count):
            try:
                # 前缀一样会被当成一批，比如testsample111同级目录下有testsample111_xx都会被读到
                transformer = sagemaker.estimator.Transformer(model_name=model_name,
                                                              instance_count=instance_count,
                                                              instance_type=instance_type,
                                                              sagemaker_session=sagemaker_session,
                                                              output_path=output_path,
                                                              accept=accept,   # 配合下面的join_source= "Input"
                                                              assemble_with=assemble_with,  # 配合下面的join_source= "Input"
                                                              )
                #
                transformer.transform(data=data, data_type=data_type,
                                      content_type=content_type, split_type=split_type,
                                      # 这里特别注意，$[a:b]是要取到b的和python的分片不太一样,所以这里不取最后一个元素，用-2
                                      # 不取第一列的用户id
                                      input_filter=input_filter,
                                      join_source=join_source,
                                      output_filter=output_filter
                                      )
                transformer.wait()
                break
            except Exception as e:
                if str(e).find("Rate exceeded") != -1:
                    continue
                else:
                    raise e
        return True


if __name__ == '__main__':  # 打版本的时候一定记得记得脱敏
    pass
