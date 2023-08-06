import sys, argparse, os, json, shutil


def installKernel():
  from jupyter_client.kernelspec import KernelSpecManager
  from IPython.utils.tempdir import TemporaryDirectory
  kernel_json = {
      "argv": ["python", "-m", "modelbit.kernel", "-f", "{connection_file}"],
      "display_name": "Modelbit Cloud (Python 3)",
      "language": "python",
      "interrupt_mode": "message"
  }
  with TemporaryDirectory() as td:
    os.chmod(td, 0o755)
    with open(os.path.join(td, 'kernel.json'), 'w') as f:
      json.dump(kernel_json, f, sort_keys=True)
    dirPath = os.path.dirname(os.path.realpath(__file__))
    for fileName in ['logo-32x32.png', 'logo-64x64.png']:
      shutil.copy(os.path.join(dirPath, "..", fileName), os.path.join(td, fileName))
    ksm = KernelSpecManager()
    ksm.install_kernel_spec(td, 'modelbit', user=True)  # type: ignore


def removeKernel():
  from jupyter_client.kernelspec import KernelSpecManager
  ksm = KernelSpecManager()
  ksm.remove_kernel_spec('modelbit')  # type: ignore


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Modelbit Setup CLI.", prog="python -m modelbit")
  subparsers = parser.add_subparsers(help="", dest="command", metavar="command")
  parser_install = subparsers.add_parser("install", help="Install the Modelbit Cloud Kernel")
  parser_remove = subparsers.add_parser("remove", help="Remove the Modelbit Cloud Kernel")

  args = parser.parse_args()

  if len(sys.argv) == 1:
    parser.print_help()
  elif args.command == "install":
    installKernel()
    print("Cloud Kernel installed successfully.")
  elif args.command == "remove":
    removeKernel()
    print("Cloud Kernel removed successfully.")
