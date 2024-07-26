import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import HomeScreen from '../screens/home-screen';
import QrCodeScreen from '../screens/qr-code';
import { Ionicons } from '@expo/vector-icons';
import ScheduleScreen from '../screens/schedule-screen';
import NotificationScreen from '../screens/notification-screen';
import DetailScreen from '../screens/schedules/details';
import { HomeStack, ProfileStack, ScheduleStack } from './stack';
import { useEffect, useState } from 'react';

const Tab = createBottomTabNavigator();

export default function HomeTabs({navigation}) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  useEffect(() => {
    // Check authentication status (e.g., read from local storage)
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
    <Tab.Navigator
        screenOptions={({ route }) => ({
            headerShown: false,
            tabBarShowLabel: true,
            tabBarStyle: {
                backgroundColor: 'black',
            },
            tabBarActiveTintColor: "yellow",
            tabBarInactiveTintColor: "grey",
            tabBarIcon: ({focused, color, size}) => {
                let iconName;
                if(route.name === 'Home') {
                    iconName = focused ? 'home': 'home-outline';
                }
                else if(route.name === 'Schedule') {
                    iconName = focused ? 'calendar': 'calendar-outline';
                }
                else if(route.name == 'Notifications') {
                  iconName = focused ? 'alarm': 'alarm-outline';
                }
                else if(route.name == 'Profile') {
                  iconName = focused ? 'person' : 'person-outline'
                }
                return <Ionicons name={iconName} size={focused ? 35: size} color={color} />
            }
            })}>
      <Tab.Screen name="Home" component={HomeStack} />
      <Tab.Screen name="Schedule" component={ScheduleStack} />
      <Tab.Screen name="Notifications" component={NotificationScreen} />
      <Tab.Screen name="Profile" component={ProfileStack} />
    </Tab.Navigator>
  );
}