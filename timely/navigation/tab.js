import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { HomeStack, NotificationStack, ProfileStack, ScheduleStack } from './stack';
import Notifications from '../screens/notification/Notifications';
import { Ionicons } from '@expo/vector-icons'; // Import Ionicons from Expo


const Tab = createBottomTabNavigator();

export const HomeTabs = ({navigation, state, descriptors}) => {
  return (
    <Tab.Navigator screenOptions={({ route }) => ({
      tabBarActiveTintColor: '#fff', // Focused tab icon color
      tabBarInactiveTintColor: '#fafafa', // Unfocused tab icon color
      tabBarStyle: { backgroundColor: '#1976d2', height: 70 }, // Tab bar background color
      headerShown: false,
      tabBarIcon: ({ focused, color, size }) => {
        let iconName;

        // Set the icon based on the route name
        if (route.name === 'Homes') {
          iconName = focused ? 'home' : 'home-outline';
        } else if (route.name === 'Schedules') {
          iconName = focused ? 'calendar' : 'calendar-outline';
        } else if (route.name === 'Notifications') {
          iconName = focused ? 'notifications' : 'notifications-outline';
        } else if (route.name === 'Profiles') {
          iconName = focused ? 'person' : 'person-outline';
        }

        return <Ionicons name={iconName} size={size} color={color} />;
      },
    })}
  >
      <Tab.Screen name="Homes" component={HomeStack} />
      <Tab.Screen name="Schedules" component={ScheduleStack} />
      <Tab.Screen name='Notifications' component={NotificationStack} />
      <Tab.Screen name='Profiles' component={ProfileStack} />
    </Tab.Navigator>
  );
}

