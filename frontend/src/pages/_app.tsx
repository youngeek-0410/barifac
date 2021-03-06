import '../styles/global.css';
import type { AppProps } from 'next/app';
import { ChakraProvider } from '@chakra-ui/react';
import React from 'react';
import theme from '../theme/theme';
import { AuthProvider } from 'context/AuthContext';
import Header from 'components/Header';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <ChakraProvider theme={theme}>
        <Header />
        <Component {...pageProps} />
      </ChakraProvider>
    </AuthProvider>
  );
}

export default MyApp;
