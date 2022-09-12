import { motion } from 'framer-motion';
import classes from './LoadingAnimation.module.css';

const loadingContainerVariants = {
  start: {
    transition: {
      staggerChildren: 0.2
    }
  },
  end: {
    transition: {
      staggerChildren: 0.2
    }
  }
};

const loadingCircleVariants = {
  start: {
    y: '50%'
  },
  end: {
    y: '150%'
  }
};

const loadingCircleTransition: any = {
  duration: 0.5,
  repeat: Infinity,
  repeatType: 'reverse',
  ease: 'easeInOut'
}

export default function LoadingAnimation() {
  return (
    <motion.div className={classes.loadingContainer}
      variants={loadingContainerVariants}
      initial='start'
      animate='end'
    >
      <motion.span className={classes.loadingCircle} variants={loadingCircleVariants} transition={loadingCircleTransition} />
      <motion.span className={classes.loadingCircle} variants={loadingCircleVariants} transition={loadingCircleTransition} />
      <motion.span className={classes.loadingCircle} variants={loadingCircleVariants} transition={loadingCircleTransition} />
    </motion.div>
  )
}
