import React from 'react';

import {
  Flex,
  Link,
  Slider,
  SliderTrack,
  SliderThumb,
  SliderFilledTrack,
  Text,
  VStack,
} from '@chakra-ui/react';
import { ArrowForwardIcon } from '@chakra-ui/icons';

export type EvaluationSliderProps = {
  evaluationUuid: string;
  name: string;
  rate: number;
  score: number;
  onChange: (score: number) => void;
};

const EvaluationSlider: React.FC<EvaluationSliderProps> = ({
  evaluationUuid,
  name,
  rate,
  score,
  onChange,
}) => {
  return (
    <VStack w='full'>
      <Flex justifyContent='space-between' w='full'>
        <Text color='gray.500'>
          {name}({rate}%)
        </Text>
        <Link href={`/score_edit/${evaluationUuid}`}>
          <ArrowForwardIcon boxSize={6} color='whiteAlpha.900' />
        </Link>
      </Flex>
      <Flex w='full'>
        <Text lineHeight={6} color='whiteAlpha.900'>
          {Math.round(score)}/ 100
        </Text>
        <Slider defaultValue={score} onChange={onChange}>
          <SliderTrack>
            <SliderFilledTrack />
          </SliderTrack>
          <SliderThumb />
        </Slider>
      </Flex>
    </VStack>
  );
};

export default EvaluationSlider;
