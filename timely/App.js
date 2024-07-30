import { View, Text } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { useEffect, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { HomeTabs } from "./navigation/tab";
import { SignInStack } from "./navigation/stack";
import { createStackNavigator } from "@react-navigation/stack";
import { StatusBar } from 'react-native';


StatusBar.setBarStyle('light-content');
const Stack = createStackNavigator();

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(0);

  useEffect(() => {
    checkAuthStatus();
  },[]);

  async function checkAuthStatus() {
    try {
      const authStatus = await AsyncStorage.getItem('userName');
      if (authStatus && authStatus.length >= 1) {
        setIsAuthenticated(5);
        console.log('User is authenticated:', authStatus);
      }
    } catch (error) {
      console.error('Error reading auth status:', error);
    }
  };
  console.log(isAuthenticated)
  return (
    <NavigationContainer>
      <Stack.Navigator
      initialRouteName={(isAuthenticated == 5) ? ("HomeTabs1") : ("SI")}
       screenOptions={{ headerShown: false }}>
        <Stack.Screen name="HomeTabs1" component={HomeTabs} />
        <Stack.Screen name="SI" component={SignInStack} />
      </Stack.Navigator>
    </NavigationContainer>
  );

  
}

export const apiURL = 'http://192.168.1.115:8000/api';
