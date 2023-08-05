from distutils.core import setup
setup(
  name = 'emlhound',       
  packages = ['emlhound'], 
  version = '0.1',     
  license='MIT',        
  description = 'EML Forensics Application',   
  author = 'needmorecowbell',                   
  author_email = 'amusciano@gmail.com',      
  url = 'https://github.com/needmorecowbell',   
  download_url = 'https://github.com/needmorecowbell/EMLHound/archive/refs/tags/0.1.tar.gz', 
  keywords = ['EML'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'fastapi',
          'uvicorn',
          'redis',
          'jinja2',
          'eml_parser[filemagic]',
          'requests',
          'watchdog'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.10',      #Specify which pyhton versions that you want to support
  ],
)
