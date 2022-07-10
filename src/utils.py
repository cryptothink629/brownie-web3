from solcx import compile_files


def get_abi_from_source(file_path):
    file_name = file_path.split('/')[-1]
    compiled_sols = compile_files([file_path], output_values=['abi', 'bin'])
    for contract_id, contract_interface in compiled_sols.items():
        if file_name in contract_id:
            print('compiling contract: ' + contract_id)
            abi = contract_interface['abi']
            bytecode = contract_interface['bin']
            return abi, bytecode
