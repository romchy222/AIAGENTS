# Start the Flask server
if __name__ == '__main__':
    from app import app
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
