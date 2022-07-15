from solcx import compile_files


def get_abi_from_source(file_path):
    file_name = file_path.split('/')[-1]
    class_name = file_name.split('.')[0]
    compiled_sols = compile_files([file_path], output_values=['abi', 'bin'])
    for contract_id, contract_interface in compiled_sols.items():
        cla_name = contract_id.split(':')[-1]
        if class_name == cla_name:
            print('compiling contract: ' + contract_id)
            abi = contract_interface['abi']
            bytecode = contract_interface['bin']
            return abi, bytecode
