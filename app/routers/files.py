from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.models import FileUpdate, User
from app.auth import get_current_user

router = APIRouter()


@router.get("", response_model=Dict[str, Any])
async def get_project_files(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get all project files"""
    # Mock file structure for now - in production this would come from E2B sandbox
    return {
        "App.js": {
            "type": "file",
            "content": """import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

export default function App() {
  return (
    <View style={styles.container}>
      <Text>Welcome to your AI-generated app!</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});"""
        },
        "package.json": {
            "type": "file",
            "content": """{
  "name": "my-app",
  "version": "1.0.0",
  "main": "node_modules/expo/AppEntry.js",
  "scripts": {
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "web": "expo start --web"
  },
  "dependencies": {
    "expo": "~49.0.0",
    "react": "18.2.0",
    "react-native": "0.72.6"
  }
}"""
        },
        "components": {
            "type": "directory",
            "children": {
                "Button.js": {
                    "type": "file",
                    "content": """import React from 'react';
import { TouchableOpacity, Text, StyleSheet } from 'react-native';

export default function Button({ title, onPress }) {
  return (
    <TouchableOpacity style={styles.button} onPress={onPress}>
      <Text style={styles.text}>{title}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: '#007AFF',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  text: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
});"""
                }
            }
        }
    }


@router.put("", response_model=Dict[str, str])
async def update_file(
    project_id: str,
    file_data: FileUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a project file"""
    # In production, this would update the file in the E2B sandbox
    # For now, just return success
    return {
        "message": f"File {file_data.file_path} updated successfully",
        "file_path": file_data.file_path
    }
