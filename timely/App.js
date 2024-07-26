import { View, Text } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { useEffect, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { HomeTabs } from "./navigation/tab";
import { SignInStack } from "./navigation/stack";
import { createStackNavigator } from "@react-navigation/stack";

const Stack = createStackNavigator();

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const authStatus = await AsyncStorage.getItem('userName');
        if (authStatus && authStatus.length >= 1) {
          setIsAuthenticated(true);
          console.log('User is authenticated:', authStatus);
        }
      } catch (error) {
        console.error('Error reading auth status:', error);
      }
    };

    checkAuthStatus();
  }, []);
  
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {isAuthenticated ? (
          <>
            <Stack.Screen name="HomeTabs1" component={HomeTabs} />
            <Stack.Screen name="SI" component={SignInStack} />
          </>
        ) : (
          <>
            <Stack.Screen name="SI" component={SignInStack} />
            <Stack.Screen name="HomeTabs1" component={HomeTabs} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );

  
}

export const apiURL = 'http://192.168.1.115:8000/api';
