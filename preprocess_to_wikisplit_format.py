import argparse

def preprocess_to_wikisplit(src_path, dst_path, output_path): 
  with open(src_path, 'r', encoding="utf-8") as f_src:
    with open(dst_path, 'r', encoding="utf-8") as f_dst:
      with open(output_path, 'w+', encoding="utf-8") as f_output:
        for s, d in zip(f_src, f_dst):
          f_output.write(s.strip() + '\t' + d.strip() + '\n')

parser = argparse.ArgumentParser()

parser.add_argument("--src-path", 
                    default=None, 
                    type=str, 
                    required=True)
parser.add_argument("--dst-path",
                    default=None,
                    type=str,
                    required=True)
parser.add_argument("--output-path",
                    default=None,
                    type=str,
                    required=True)

args = parser.parse_args()

preprocess_to_wikisplit(args.src_path, args.dst_path, args.output_path)
