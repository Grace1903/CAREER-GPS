import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('uploads/resumes', exist_ok=True)
    
    app.run(debug=False, host='0.0.0.0', port=5000)