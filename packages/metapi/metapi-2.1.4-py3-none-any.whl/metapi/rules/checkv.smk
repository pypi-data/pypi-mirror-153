if config["params"]["checkv"]["do"]:
    rule checkv: 
        input:

        output:

        conda:
            config["envs"]["checkv"]
        shell:
            '''
            checkv end_to_end 

            '''