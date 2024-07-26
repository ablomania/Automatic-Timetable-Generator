import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, TextInput, View, Platform, Button, ScrollView, SafeAreaView, TouchableOpacity } from 'react-native';
import { useState, useEffect } from "react";
import { NavigationContainer, useNavigation } from '@react-navigation/native';
import { AppStack, HomeStack, SignInStacks } from './navigation/stack';
import 'react-native-gesture-handler';
import HomeTabs from './navigation/tabs';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator()
export default function App() {

  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const authStatus = await AsyncStorage.getItem('userName');
        if(authStatus.length >= 1);
          setIsAuthenticated(true);
          console.log(authStatus)
      } catch (error) {
        console.error('Error reading auth status:', error);
      }
    };

    checkAuthStatus();
  }, []);
  return (
    <NavigationContainer>
      {isAuthenticated ? (
        <HomeTabs /> 
        ) : (
        <SignInStacks />
        )}
    </NavigationContainer>
    
  );
}

export const apiURL = 'http://192.168.1.161:8000/api';

const styles = StyleSheet.create({
  input: {
    height: 40,
    margin: 12,
    borderWidth:1,
    borderColor: "blue",
    padding: 10,
  }
})