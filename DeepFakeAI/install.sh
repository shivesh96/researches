git clone https://github.com/s0md3v/roop.git
%cd roop
pip install -r requirements.txt
pip3 install -r requirements.txt --use-pep517


wget https://civitai.com/api/download/models/85159 -O inswapper_128.onnx
wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth -O GFPGANv1.4.pth


pip uninstall onnxruntime onnxruntime-gpu -y
pip install torch torchvision torchaudio --force-reinstall --index-url https://download.pytorch.org/whl/cu118
pip install onnxruntime-gpu

brew install ffmpeg

python run.py --target /Users/shivesh96/Desktop/DeepFakeAI/maleModel.jpeg  --source /Users/shivesh96/Desktop/DeepFakeAI/shivesh.jpg -o /content/swapped.mp4 --execution-provider {cpu,cuda} --frame-processor face_swapper face_enhancer

python3 run.py --target /Users/shivesh96/Desktop/DeepFakeAI/maleModel.jpeg  --source /Users/shivesh96/Desktop/DeepFakeAI/shivesh.jpg -o /content/swapped.jpg --execution-provider cpu --frame-processor face_swapper


sudo python3 run.py --target /Users/shivesh96/Desktop/DeepFakeAI/maleModel.jpeg  --source /Users/shivesh96/Desktop/DeepFakeAI/shivesh.jpg -o /Users/shivesh96/Desktop/DeepFakeAI/swapped.jpg --execution-provider cpu --frame-processor face_swapper face_enhancer



# to change file
whoami
sudo chown -R {shivesh96} DeepFakeAI