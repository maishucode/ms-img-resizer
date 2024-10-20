#!/bin/bash

# Clone the repository into the home directory
# cd /home/ec2-user
# git clone https://github.com/maishucode/simple-image-resizer.git

# Install pyenv
curl https://pyenv.run | bash

# Update shell configuration
{
  echo 'export PATH="$HOME/.pyenv/bin:$PATH"'
  echo 'eval "$(pyenv init --path)"'
  echo 'eval "$(pyenv init -)"'
  echo 'eval "$(pyenv virtualenv-init -)"'
} >> ~/.bashrc

# Reload shell configuration
source ~/.bashrc

# Install Python 3.12.5 using pyenv
pyenv install 3.12.5

# Set Python 3.12.5 as the global version
pyenv global 3.12.5

# Verify the Python installation
python --version